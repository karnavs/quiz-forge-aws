const SESSIONS_TABLE = process.env.SESSIONS_TABLE || "QuizForge-Sessions";
const ATTEMPTS_TABLE = process.env.ATTEMPTS_TABLE || "QuizForge-Attempts";
const IS_OFFLINE = process.env.IS_OFFLINE === "true" || !process.env.AWS_REGION;

let ddbDocClient = null;
const memorySessions = new Map();
const memoryAttempts = [];

if (!IS_OFFLINE) {
  try {
    const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
    const { DynamoDBDocumentClient } = require("@aws-sdk/lib-dynamodb");
    const client = new DynamoDBClient({});
    ddbDocClient = DynamoDBDocumentClient.from(client);
  } catch (err) {
    console.warn("DynamoDB SDK not present or failed to initialize, using in-memory store:", err.message);
  }
}

async function saveQuizSession(session) {
  // Ensure both quizId and quizID exist to match either table partition key
  session.quizId = session.quizId;
  session.quizID = session.quizId;

  if (ddbDocClient) {
    try {
      const { PutCommand } = require("@aws-sdk/lib-dynamodb");
      await ddbDocClient.send(new PutCommand({
        TableName: SESSIONS_TABLE,
        Item: session,
      }));
      return session;
    } catch (err) {
      console.warn("DynamoDB write failed (falling back to memory):", err.message);
    }
  }
  memorySessions.set(session.quizId, JSON.parse(JSON.stringify(session)));
  return session;
}

async function getQuizSession(quizId) {
  if (ddbDocClient) {
    try {
      const { GetCommand } = require("@aws-sdk/lib-dynamodb");
      // Try quizID first, then quizId
      let result = await ddbDocClient.send(new GetCommand({
        TableName: SESSIONS_TABLE,
        Key: { quizID: quizId },
      })).catch(() => null);

      if (!result?.Item) {
        result = await ddbDocClient.send(new GetCommand({
          TableName: SESSIONS_TABLE,
          Key: { quizId: quizId },
        })).catch(() => null);
      }

      if (result?.Item) return result.Item;
    } catch (err) {
      console.warn("DynamoDB read failed (falling back to memory):", err.message);
    }
  }
  return memorySessions.get(quizId) || null;
}

async function markSessionCompleted(quizId) {
  if (ddbDocClient) {
    try {
      const { UpdateCommand } = require("@aws-sdk/lib-dynamodb");
      await ddbDocClient.send(new UpdateCommand({
        TableName: SESSIONS_TABLE,
        Key: { quizID: quizId },
        UpdateExpression: "SET #st = :status",
        ExpressionAttributeNames: { "#st": "status" },
        ExpressionAttributeValues: { ":status": "COMPLETED" },
      })).catch(async () => {
        await ddbDocClient.send(new UpdateCommand({
          TableName: SESSIONS_TABLE,
          Key: { quizId: quizId },
          UpdateExpression: "SET #st = :status",
          ExpressionAttributeNames: { "#st": "status" },
          ExpressionAttributeValues: { ":status": "COMPLETED" },
        }));
      });
    } catch (err) {
      console.warn("DynamoDB update failed (falling back to memory):", err.message);
    }
  }
  const session = memorySessions.get(quizId);
  if (session) {
    session.status = "COMPLETED";
  }
}

async function saveQuizAttempt(attempt) {
  if (ddbDocClient) {
    try {
      const { PutCommand } = require("@aws-sdk/lib-dynamodb");
      await ddbDocClient.send(new PutCommand({
        TableName: ATTEMPTS_TABLE,
        Item: attempt,
      }));
      return attempt;
    } catch (err) {
      console.warn("DynamoDB attempt save failed (falling back to memory):", err.message);
    }
  }
  memoryAttempts.unshift(JSON.parse(JSON.stringify(attempt)));
  if (memoryAttempts.length > 20) memoryAttempts.pop();
  return attempt;
}

async function getRecentAttempts(limit = 10) {
  if (ddbDocClient) {
    try {
      const { ScanCommand } = require("@aws-sdk/lib-dynamodb");
      const result = await ddbDocClient.send(new ScanCommand({
        TableName: ATTEMPTS_TABLE,
        Limit: limit,
      }));
      return (result.Items || []).sort((a, b) => (b.completedAt || 0) - (a.completedAt || 0));
    } catch (err) {
      console.warn("Error scanning attempts table:", err.message);
    }
  }
  return memoryAttempts.slice(0, limit);
}

module.exports = {
  saveQuizSession,
  getQuizSession,
  markSessionCompleted,
  saveQuizAttempt,
  getRecentAttempts,
};
