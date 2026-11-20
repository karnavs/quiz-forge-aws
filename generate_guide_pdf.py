import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = r"C:\Users\Karna\Downloads\QuizForge_AWS_Beginners_Guide.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (on pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 750, "QuizForge — Complete AWS Serverless Beginner Guide & Presentation Script")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "QuizForge Project · Karna, Chinmay & Akash · CloudFront & Lambda")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#2563eb"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    box_style = ParagraphStyle(
        'BoxText',
        parent=body_style,
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#0f172a")
    )

    script_speaker = ParagraphStyle(
        'SpeakerHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=2,
        keepWithNext=True
    )

    script_line = ParagraphStyle(
        'ScriptLine',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5
    )

    script_cue = ParagraphStyle(
        'ScriptCue',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2563eb"),
        spaceAfter=4
    )
    
    story = []

    # Title Banner
    story.append(Paragraph("QuizForge: AWS Serverless Guide", title_style))
    story.append(Paragraph("A Step-by-Step Walkthrough & 5-Minute 3-Person Presentation Script (Karna, Chinmay, Akash)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    # Architecture Overview Box
    intro_html = """
    <b>What are we building?</b> We are creating a live trivia game hosted globally on Amazon Web Services (AWS). 
    Whenever a player selects a topic and clicks 'Start Quiz', AWS queries questions over the internet, locks the secret answers on the server (so players can't cheat with inspect element!), scores the answers, and serves the whole website over secure HTTPS.
    """
    story.append(Table([[Paragraph(intro_html, box_style)]], colWidths=[504], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bfdbfe")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    # Part 1: The 5 Superheroes
    story.append(Paragraph("Part 1: The 5 AWS Superheroes Explained in Plain English", h1_style))

    heroes_data = [
        [Paragraph("<b>AWS Service</b>", body_style), Paragraph("<b>Kid-Friendly Metaphor</b>", body_style), Paragraph("<b>What It Does in QuizForge</b>", body_style)],
        [Paragraph("<b>Amazon S3</b>", body_style), Paragraph("The Locker / Toy Box", body_style), Paragraph("Stores the website files (index.html, style.css, app.js) safely in the cloud.", body_style)],
        [Paragraph("<b>AWS Lambda</b>", body_style), Paragraph("The Robot Brain", body_style), Paragraph("Runs code only when clicked. Fetches trivia, shuffles choices, and calculates scores.", body_style)],
        [Paragraph("<b>Amazon DynamoDB</b>", body_style), Paragraph("The Digital Notebook", body_style), Paragraph("Remembers quiz sessions and high scores so answers are never lost.", body_style)],
        [Paragraph("<b>Function URL</b>", body_style), Paragraph("The Secret Intercom", body_style), Paragraph("A direct, free HTTPS web address allowing S3 to talk straight to Lambda.", body_style)],
        [Paragraph("<b>Amazon CloudFront</b>", body_style), Paragraph("The Global Courier", body_style), Paragraph("Delivers your website instantly from servers around the globe with HTTPS (*.cloudfront.net).", body_style)],
    ]
    t = Table(heroes_data, colWidths=[105, 135, 264])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Part 2: Step-by-Step Blueprint
    story.append(Paragraph("Part 2: The Exact Step-by-Step Deployment Guide", h1_style))
    
    steps = [
        ("Step 1: Wake Up Your AWS Academy Lab", [
            "Go to <b>https://awsacademy.instructure.com/</b> and sign in with your student email.",
            "Open your course &rarr; scroll down to <b>Modules</b> &rarr; click <b>Sandbox environment</b>.",
            "Click <b>Start Lab</b>. Wait 1-2 minutes until the status dot turns green 🟢.",
            "Click the active <b>AWS</b> link. This opens the real AWS Management Console in <i>us-east-1 (N. Virginia)</i>."
        ]),
        ("Step 2: Create the DynamoDB Database Table", [
            "In the top search bar, type <b>DynamoDB</b> and click it.",
            "Click <b>Create table</b> &rarr; Name: <b>QuizForge-Sessions</b> | Partition key: <b>quizId</b> (String).",
            "Leave everything else default and click <b>Create table</b>."
        ]),
        ("Step 3: Create the AWS Lambda Backend Function", [
            "In top search bar, search <b>Lambda</b> &rarr; click <b>Create function</b>.",
            "Function name: <b>QuizForge-Backend</b> | Runtime: <b>Node.js 20.x</b> (or 22.x/24.x).",
            "Click <b>▶ Additional settings</b> &rarr; toggle ON <b>Custom execution role</b> &rarr; choose <b>lambda-run-role</b>.",
            "Click <b>Create Event Function</b>."
        ]),
        ("Step 4: Upload Backend Code & Increase Timeout", [
            "In Lambda &rarr; <b>Code source</b> &rarr; <b>Update ▾</b> &rarr; <b>.zip file</b> &rarr; upload <code>backend.zip</code> &rarr; <b>Save</b>.",
            "Go to <b>Configuration</b> tab &rarr; <b>General configuration</b> &rarr; <b>Edit</b> &rarr; Timeout: <b>10 seconds</b> &rarr; <b>Save</b>."
        ]),
        ("Step 5: Turn On Lambda Function URL (Public HTTPS Endpoint)", [
            "Under <b>Configuration</b> &rarr; <b>Function URL</b> &rarr; <b>Create function URL</b>.",
            "Auth type: <b>NONE</b> | <b>UNCHECK</b> Configure cross-origin resource sharing (CORS) &rarr; <b>Save</b>.",
            "Go to <b>Permissions</b> &rarr; Resource-based policy &rarr; <b>Add permissions</b> &rarr; select <b>lambda:InvokeFunction</b> with Principal: <code>*</code> &rarr; <b>Save</b>."
        ]),
        ("Step 6: Create S3 Website Bucket & Upload Frontend", [
            "Search <b>S3</b> &rarr; <b>Create bucket</b> &rarr; Name: <b>quizforge-app-[account-id]</b>.",
            "<b>UNCHECK</b> 'Block all public access' and check acknowledgment box &rarr; <b>Create bucket</b>.",
            "Properties &rarr; <b>Static website hosting</b> &rarr; <b>Enable</b> &rarr; index: <code>index.html</code> &rarr; <b>Save</b>.",
            "Permissions &rarr; <b>Bucket policy</b> &rarr; paste public read policy &rarr; <b>Save</b>.",
            "Objects tab &rarr; <b>Upload</b> &rarr; add <code>index.html</code>, <code>style.css</code>, <code>app.js</code> &rarr; <b>Upload</b>."
        ]),
        ("Step 7: Setup CloudFront for the Global *.cloudfront.net URL", [
            "Search <b>CloudFront</b> &rarr; <b>Create distribution</b>.",
            "Plan: Select <b>Pay as you go</b> (Crucial: Avoids WAF firewall restrictions).",
            "Name: <b>QuizForge-CDN</b> | Origin: choose S3 bucket &rarr; click <b>Use website endpoint</b>.",
            "Security: Select <b>Do not enable security protections</b> &rarr; click <b>Create distribution</b>.",
            "Under Settings on new distribution &rarr; <b>Edit</b> &rarr; Default root object: <b>index.html</b> &rarr; <b>Save changes</b>."
        ])
    ]

    for title, items in steps:
        story.append(Paragraph(title, h2_style))
        for item in items:
            story.append(Paragraph(f"• {item}", bullet_style))
        story.append(Spacer(1, 2))

    story.append(PageBreak())

    # Part 3: The Complete Real-World Error Handbook
    story.append(Paragraph("Part 3: The 'Trap & Fix' Handbook (All Errors We Conquered!)", h1_style))
    story.append(Paragraph("Every cloud engineer hits errors. Here are the 9 exact traps we encountered today and why they happened:", body_style))

    traps = [
        ("Trap 1: The 'Bad Request' Sign-in Error",
         "Entering student college email directly into standard AWS Root login.",
         "Student accounts are managed through university AWS Academy / Canvas portals, NOT standard AWS root credentials.",
         "Always log into <b>https://awsacademy.instructure.com/</b> first, start the lab, and click the AWS green button."),
        
        ("Trap 2: The 'iam:PassRole' Permission Denied Error",
         "Trying to use default roles or creating new IAM roles inside Lambda.",
         "AWS Academy locks down identity creation so students cannot create arbitrary cloud roles.",
         "Select the pre-existing role <b>lambda-run-role</b> under 'Use an existing role'."),
        
        ("Trap 3: The 'apigateway:PUT' Restricted Error",
         "Attempting to build an HTTP API in API Gateway.",
         "University course permissions often disable API Gateway creation to prevent unexpected routing bugs.",
         "Bypass API Gateway completely by using <b>AWS Lambda Function URL</b> — it provides a free, instant HTTPS address directly from Lambda!"),

        ("Trap 4: The Function URL 403 Forbidden Error",
         "Opening the Function URL returned a 403 Forbidden message.",
         "Even with Auth 'NONE', AWS requires a resource policy allowing anonymous visitors to invoke the URL.",
         "Add a statement in the Permissions tab granting <b>lambda:InvokeFunction</b> with Principal: <code>*</code>."),

        ("Trap 5: The S3 'NoSuchWebsiteConfiguration' 404 Error",
         "Visiting the S3 link gave a 404 XML code error.",
         "S3 is a file storage drive by default. It only acts like a web server when told to.",
         "In S3 Bucket Properties &rarr; scroll to bottom &rarr; Enable <b>Static website hosting</b> with <code>index.html</code>."),

        ("Trap 6: The Double CORS Header Bug ('*, *')",
         "Browser console threw: <i>The 'Access-Control-Allow-Origin' header contains multiple values '*, *'</i>.",
         "AWS Function URL CORS was enabled in console, AND our Lambda code returned CORS headers too. The browser saw two asterisks and blocked the request for safety!",
         "Turn OFF the CORS toggle in the AWS Lambda Function URL settings, and let our clean backend code handle the header."),

        ("Trap 7: Lambda 500 Error (Base64 Body & DynamoDB Permissions)",
         "Clicking Start Quiz gave an Internal Server Error 500.",
         "Function URLs automatically base64-encode POST requests. Also, some lab roles have strict DynamoDB write policies.",
         "Added Base64 decoding in Lambda handler (<code>Buffer.from(raw, 'base64')</code>) and added an automated fallback to in-memory sessions if DynamoDB writes are restricted."),

        ("Trap 8: The CloudFront 'wafv2:CreateWebACL' Error",
         "CloudFront creation wizard failed at Step 4 with a permission denied error.",
         "The new CloudFront wizard defaults to a 'Flat-rate plan' which automatically tries to create a paid AWS WAF firewall.",
         "At Step 1, select <b>Pay as you go</b>. At Step 4, choose <b>Do not enable security protections</b>."),

        ("Trap 9: CloudFront Blank Screen (Missing Default Root Object)",
         "Visiting the CloudFront domain didn't open the homepage.",
         "CloudFront didn't know which file was the main landing page because 'Default root object' was empty.",
         "In CloudFront Settings &rarr; Edit &rarr; set <b>Default root object</b> to <b>index.html</b>.")
    ]

    for title, err_symptom, why_it_happens, how_to_fix in traps:
        content = f"""
        <b>{title}</b><br/>
        <b>Symptom:</b> {err_symptom}<br/>
        <b>Why it happens:</b> {why_it_happens}<br/>
        <b>The Fix:</b> {how_to_fix}
        """
        story.append(Table([[Paragraph(content, box_style)]], colWidths=[504], style=[
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # =========================================================================
    # PART 4: 5-MINUTE 3-PERSON PRESENTATION SCRIPT
    # =========================================================================
    story.append(Paragraph("Part 4: 5-Minute 3-Person Presentation Script", h1_style))
    story.append(Paragraph("A polished, rehearsed presentation script divided between <b>Karna</b>, <b>Chinmay</b>, and <b>Akash</b>, timed to exactly 5 minutes with slide transitions.", subtitle_style))

    # --- SPEAKER 1: KARNA ---
    story.append(Paragraph("SPEAKER 1: KARNA (Minutes 0:00 – 1:40) · Slides 1 & 2", script_speaker))
    story.append(Paragraph("<i>[Slide 1: Intro is on the projector]</i>", script_cue))
    story.append(Paragraph("<b>Karna:</b> \"Good morning everyone and respected faculty. Today, my teammates Chinmay, Akash, and I are excited to present our project: <b>QuizForge</b> — a high-performance, serverless trivia application architected entirely on Amazon Web Services.", script_line))
    story.append(Paragraph("When building online quiz applications, traditional architectures rely on dedicated servers that idle 95% of the time, burning compute costs. Worse, many web quizzes store answer keys directly in client-side JavaScript, meaning any student can simply press F12 and inspect the answers. We designed QuizForge to solve both problems using modern cloud-native serverless architecture with zero server management and strict anti-cheat scoring.", script_line))
    story.append(Paragraph("<i>[Transition to Slide 2: Services Used]</i>", script_cue))
    story.append(Paragraph("<b>Karna:</b> On Slide 2, you see the core building blocks of our solution: First, <b>Amazon S3</b> serves as our ultra-durable static website repository. Second, <b>Amazon CloudFront</b> provides a global Content Delivery Network, delivering our site through edge locations worldwide with HTTPS under our custom domain. Third, <b>AWS Lambda</b> powers our backend logic, executing Node.js code strictly on demand. Fourth, <b>Amazon DynamoDB</b> provides low-latency NoSQL persistence for quiz sessions and scores. Finally, we dynamically pull question banks from the <b>Open Trivia Database API</b>. Now, I will hand over to Chinmay to walk you through the end-to-end request lifecycle and demonstrate how these pieces interact.\"", script_line))

    story.append(Spacer(1, 8))

    # --- SPEAKER 2: CHINMAY ---
    story.append(Paragraph("SPEAKER 2: CHINMAY (Minutes 1:40 – 3:20) · Slide 3 & Live Demo", script_speaker))
    story.append(Paragraph("<i>[Slide 3: Architecture & Request Flow is on the projector]</i>", script_cue))
    story.append(Paragraph("<b>Chinmay:</b> \"Thank you, Karna. On Slide 3, we illustrate the exact lifecycle of a user request in QuizForge:", script_line))
    story.append(Paragraph("1. When a user navigates to our live CloudFront URL, CloudFront routes the request to our S3 bucket and returns our minimalist, unslop single-page application directly to the browser.<br/>"
                           "2. When the user selects a category and difficulty and clicks 'Start Quiz', a POST request is sent directly to our <b>AWS Lambda Function URL</b>.<br/>"
                           "3. Lambda queries OpenTDB, parses the trivia response, decodes special HTML entities, shuffles the answer options, and generates a unique cryptographic quiz ID.<br/>"
                           "4. <b>Here is our key security feature:</b> Lambda locks the correct answer key safely inside DynamoDB (or server memory). The response sent back to the browser contains ONLY the questions and shuffled options. Even if a user opens Developer Tools, the answer key does not exist on their machine!<br/>"
                           "5. Once the user submits, Lambda compares the choices against the stored key, calculates the exact percentage score, records the completed attempt, and returns the detailed question review.", script_line))
    story.append(Paragraph("<i>[Chinmay quickly opens the live browser tab: https://d1p562n93qruz1.cloudfront.net]</i>", script_cue))
    story.append(Paragraph("<b>Chinmay:</b> As you can see live on screen, the interface is minimal, fast, and responsive. I select History, 5 questions, click Start Quiz, select options, and submit — immediately receiving verified, server-scored results. I'll now hand over to Akash to explain the technical hurdles we solved and our conclusions.\"", script_line))

    story.append(Spacer(1, 8))

    # --- SPEAKER 3: AKASH ---
    story.append(Paragraph("SPEAKER 3: AKASH (Minutes 3:20 – 5:00) · Slides 4 & 5", script_speaker))
    story.append(Paragraph("<i>[Transition to Slide 4: Major Findings]</i>", script_cue))
    story.append(Paragraph("<b>Akash:</b> \"Thank you, Chinmay. Deploying on real cloud infrastructure inevitably presents real-world engineering constraints, and on Slide 4 we highlight our major findings:", script_line))
    story.append(Paragraph("First, in university lab environments, standard API Gateway creation was restricted by IAM policy. Rather than getting blocked, we pivoted to <b>AWS Lambda Function URLs</b>, which provided a native, high-speed HTTPS endpoint with zero additional services or costs.<br/>"
                           "Second, we diagnosed a subtle CORS anomaly: enabling CORS in the AWS console while returning CORS headers in code caused browsers to receive duplicate asterisks ('*, *'), triggering cross-origin blocks. Removing the console toggle resolved it instantly.<br/>"
                           "Third, Function URLs automatically base64-encode POST bodies; our Lambda backend was engineered to detect and decode base64 payloads to prevent JSON parsing errors.", script_line))
    story.append(Paragraph("<i>[Transition to Slide 5: Wrap Up & Conclusion]</i>", script_cue))
    story.append(Paragraph("<b>Akash:</b> To wrap up on Slide 5: QuizForge demonstrates that modern cloud software does not require expensive, dedicated servers running 24/7. Our application costs exactly <b>$0.00</b> on the AWS Free Tier, scales automatically from a single student to thousands of concurrent users, and demonstrates clean separation of concerns across S3, CloudFront, Lambda, and DynamoDB.<br/>"
                           "Our live deployment is accessible right now at <b>https://d1p562n93qruz1.cloudfront.net</b>. Thank you, and we welcome any questions from the panel!\"", script_line))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully updated at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
