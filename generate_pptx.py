import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PPTX_PATH = r"C:\Users\Karna\Downloads\QuizForge_Presentation.pptx"

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Clean Unslop Aesthetic (Dark Minimalist)
    COLOR_BG = RGBColor(9, 9, 11)           # #09090b
    COLOR_SURFACE = RGBColor(18, 18, 21)     # #121215
    COLOR_BORDER = RGBColor(39, 39, 42)      # #27272a
    COLOR_TEXT = RGBColor(250, 250, 250)     # #fafafa
    COLOR_MUTED = RGBColor(161, 161, 170)    # #a1a1aa
    COLOR_SUBTLE = RGBColor(113, 113, 122)   # #71717a
    COLOR_ACCENT = RGBColor(56, 189, 248)    # #38bdf8

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="QUIZFORGE · AWS SERVERLESS"):
        # Category Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_SUBTLE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.95), Inches(11.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT

    # -------------------------------------------------------------------------
    # SLIDE 1: INTRO
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent Dot & Tag
    dot = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), Inches(2.2), Inches(0.18), Inches(0.18))
    dot.fill.solid()
    dot.fill.fore_color.rgb = COLOR_ACCENT
    dot.line.fill.background()

    tag_box = s1.shapes.add_textbox(Inches(1.15), Inches(2.1), Inches(8), Inches(0.4))
    p_tag = tag_box.text_frame.paragraphs[0]
    p_tag.text = "CLOUD ARCHITECTING CAPSTONE PROJECT"
    p_tag.font.name = "Arial"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_SUBTLE

    # Big Title
    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.5), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "QuizForge"
    p.font.name = "Arial"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT

    p2 = tf.add_paragraph()
    p2.text = "A Serverless Trivia Platform Built on Amazon Web Services"
    p2.font.name = "Arial"
    p2.font.size = Pt(22)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_before = Pt(8)

    # Team Card at Bottom
    team_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.4))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = COLOR_SURFACE
    team_card.line.color.rgb = COLOR_BORDER
    team_card.line.width = Pt(1)

    tb_team = s1.shapes.add_textbox(Inches(1.1), Inches(5.15), Inches(11.1), Inches(1.1))
    tf_team = tb_team.text_frame
    p_lead = tf_team.paragraphs[0]
    p_lead.text = "PROJECT TEAM & PRESENTERS"
    p_lead.font.name = "Arial"
    p_lead.font.size = Pt(10)
    p_lead.font.bold = True
    p_lead.font.color.rgb = COLOR_SUBTLE

    p_members = tf_team.add_paragraph()
    p_members.text = "Karna  ·  Chinmay  ·  Akash"
    p_members.font.name = "Arial"
    p_members.font.size = Pt(18)
    p_members.font.bold = True
    p_members.font.color.rgb = COLOR_TEXT
    p_members.space_before = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 2: SERVICES USED
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "AWS Services & External Components")

    services = [
        ("AWS Lambda", "Serverless Compute", "Executes event-driven Node.js backend logic on demand with zero server management. Handles OpenTDB requests, sanitizes entities, and scores quizzes server-side."),
        ("Amazon S3", "Static Hosting", "Stores built frontend assets (HTML, CSS, JS) in a dedicated bucket configured for static website hosting with least-privilege public read permissions."),
        ("Amazon CloudFront", "Global CDN", "Distributes the web application across edge locations worldwide with low-latency HTTPS delivery under a unified *.cloudfront.net domain."),
        ("Amazon DynamoDB", "NoSQL Database", "Stores active quiz sessions and user attempt records with pay-per-request on-demand capacity and automated time-to-live (TTL) expiration."),
        ("OpenTDB API", "Dynamic Question Bank", "Free external REST API supplying verified multiple-choice questions across diverse categories and difficulties with strict rate-limit handling.")
    ]

    card_w = Inches(2.18)
    card_h = Inches(4.7)
    start_x = Inches(0.8)
    spacing = Inches(0.2)

    for i, (name, role, desc) in enumerate(services):
        cx = start_x + i * (card_w + spacing)
        cy = Inches(1.9)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_SURFACE
        card.line.color.rgb = COLOR_BORDER
        card.line.width = Pt(1)

        tbox = s2.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.2), card_w - Inches(0.3), card_h - Inches(0.4))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_role = tf.paragraphs[0]
        p_role.text = role.upper()
        p_role.font.name = "Arial"
        p_role.font.size = Pt(9)
        p_role.font.bold = True
        p_role.font.color.rgb = COLOR_ACCENT

        p_name = tf.add_paragraph()
        p_name.text = name
        p_name.font.name = "Arial"
        p_name.font.size = Pt(15)
        p_name.font.bold = True
        p_name.font.color.rgb = COLOR_TEXT
        p_name.space_before = Pt(4)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_MUTED
        p_desc.space_before = Pt(12)

    # -------------------------------------------------------------------------
    # SLIDE 3: HOW WE HAVE USED THEM (ARCHITECTURE & LIFECYCLE)
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Architecture & End-to-End Request Flow")

    steps = [
        ("1. User Access", "Browser & CloudFront", "Client accesses https://d1p562n93qruz1.cloudfront.net. CloudFront routes traffic to S3 edge storage to deliver the clean SPA interface over HTTPS."),
        ("2. Quiz Generation", "Client &rarr; Lambda URL", "When user clicks 'Start Quiz', a POST request triggers Lambda Function URL. Lambda queries OpenTDB, shuffles answer choices, and generates a unique quiz ID."),
        ("3. Secret Locking", "Lambda &rarr; DynamoDB", "Lambda stores questions alongside secret correct answers in DynamoDB (or memory). Only sanitized questions WITHOUT answers return to the browser."),
        ("4. Server-Side Scoring", "Submission & Verification", "On submission, Lambda compares user choices against the stored key, calculates percentage score, marks attempt completed, and returns full answer review.")
    ]

    for i, (title, sub, details) in enumerate(steps):
        row_y = Inches(1.9) + i * Inches(1.18)
        bar = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), row_y, Inches(11.7), Inches(1.05))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_SURFACE
        bar.line.color.rgb = COLOR_BORDER
        bar.line.width = Pt(1)

        tbox = s3.shapes.add_textbox(Inches(1.1), row_y + Inches(0.12), Inches(11.1), Inches(0.85))
        tf = tbox.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{title.upper()}  —  {sub}"
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT

        p2 = tf.add_paragraph()
        p2.text = details
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_before = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 4: MAJOR FINDINGS & TECHNICAL LEARNINGS
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Major Findings & Overcoming Real-World Cloud Constraints")

    findings = [
        ("Lambda Function URL vs API Gateway", "University lab IAM restrictions disabled apigateway:PUT. We solved this by using AWS Lambda Function URLs, eliminating extra gateway costs and creating direct, native HTTPS endpoints."),
        ("CORS Double-Header Anomaly", "Enabling CORS in the AWS Lambda console while returning CORS headers in code caused browsers to receive 'Access-Control-Allow-Origin: *, *'. Disabling the console toggle fixed cross-origin communication."),
        ("Base64 Payload Handling", "Lambda Function URLs automatically encode POST bodies from web clients in Base64. Our backend parses event.isBase64Encoded to reliably parse JSON requests and prevent 500 errors."),
        ("Anti-Cheat Cloud Security", "Calculating scores on Lambda rather than in client JavaScript prevents players from inspecting DOM or network tab payloads to find correct answers prior to submission.")
    ]

    col_w = Inches(5.7)
    col_h = Inches(2.25)
    positions = [
        (Inches(0.8), Inches(1.9)),
        (Inches(6.8), Inches(1.9)),
        (Inches(0.8), Inches(4.35)),
        (Inches(6.8), Inches(4.35))
    ]

    for i, (title, desc) in enumerate(findings):
        x, y = positions[i]
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, col_h)
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_SURFACE
        box.line.color.rgb = COLOR_BORDER
        box.line.width = Pt(1)

        tbox = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), col_w - Inches(0.5), col_h - Inches(0.4))
        tf = tbox.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_MUTED
        p2.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 5: WRAP UP & CONCLUSION
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Wrap Up & Key Takeaways")

    # Big Summary Card
    sum_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.7), Inches(2.4))
    sum_box.fill.solid()
    sum_box.fill.fore_color.rgb = COLOR_SURFACE
    sum_box.line.color.rgb = COLOR_BORDER
    sum_box.line.width = Pt(1)

    tf_sum = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.1), Inches(2.0)).text_frame
    tf_sum.word_wrap = True

    p_sum_h = tf_sum.paragraphs[0]
    p_sum_h.text = "CORE PROJECT VALUE"
    p_sum_h.font.name = "Arial"
    p_sum_h.font.size = Pt(10)
    p_sum_h.font.bold = True
    p_sum_h.font.color.rgb = COLOR_ACCENT

    p_sum_t = tf_sum.add_paragraph()
    p_sum_t.text = "Serverless Architectures Eliminate Infrastructure Overhead"
    p_sum_t.font.name = "Arial"
    p_sum_t.font.size = Pt(20)
    p_sum_t.font.bold = True
    p_sum_t.font.color.rgb = COLOR_TEXT
    p_sum_t.space_before = Pt(4)

    p_sum_d = tf_sum.add_paragraph()
    p_sum_d.text = "QuizForge demonstrates that modern cloud applications require zero dedicated virtual machines, zero always-on databases, and zero idle costs ($0.00). By combining Amazon S3 static hosting, CloudFront global edge delivery, and Lambda event-driven compute, the application scales from 1 player to thousands with high availability and instant responsiveness."
    p_sum_d.font.name = "Arial"
    p_sum_d.font.size = Pt(11)
    p_sum_d.font.color.rgb = COLOR_MUTED
    p_sum_d.space_before = Pt(10)

    # Live URL Banner
    url_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(11.7), Inches(1.8))
    url_box.fill.solid()
    url_box.fill.fore_color.rgb = RGBColor(15, 23, 42)
    url_box.line.color.rgb = RGBColor(56, 189, 248)
    url_box.line.width = Pt(1.5)

    tf_url = s5.shapes.add_textbox(Inches(1.1), Inches(4.8), Inches(11.1), Inches(1.4)).text_frame
    tf_url.word_wrap = True

    p_live = tf_url.paragraphs[0]
    p_live.text = "LIVE DEPLOYMENT ENDPOINT"
    p_live.font.name = "Arial"
    p_live.font.size = Pt(10)
    p_live.font.bold = True
    p_live.font.color.rgb = COLOR_ACCENT

    p_link = tf_url.add_paragraph()
    p_link.text = "https://d1p562n93qruz1.cloudfront.net"
    p_link.font.name = "Arial"
    p_link.font.size = Pt(22)
    p_link.font.bold = True
    p_link.font.color.rgb = COLOR_TEXT
    p_link.space_before = Pt(4)

    p_sub = tf_url.add_paragraph()
    p_sub.text = "Questions powered by Open Trivia Database (OpenTDB) · MIT License"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = COLOR_SUBTLE
    p_sub.space_before = Pt(6)

    prs.save(PPTX_PATH)
    print(f"Presentation saved to {PPTX_PATH}")

if __name__ == "__main__":
    create_presentation()
