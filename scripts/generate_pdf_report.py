import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Spotify Tracks EDA — Comprehensive Subjective Analysis & Strategic Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL — Music Direction & Audio Engineering Intelligence")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    pdf_path = "Spotify_EDA_Subjective_Answers.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1DB954'),
        alignment=TA_LEFT
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748B'),
        alignment=TA_LEFT
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    q_title_style = ParagraphStyle(
        'QuestionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0369A1'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        alignment=TA_JUSTIFY,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=14,
        spaceAfter=2
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # Title Block
    story.append(Paragraph("Spotify Tracks Exploratory Data Analysis", title_style))
    story.append(Paragraph("Comprehensive Subjective Answers & Strategic Audio Engineering Report", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Target Persona:</b> Music Director / Mixing & Mastering Engineer &nbsp;|&nbsp; <b>Validated Sample:</b> 62,204 Tracks (1971–2024)", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1DB954'), spaceAfter=12))

    # Executive Summary Card
    exec_text = (
        "<b>Executive Context:</b> This document provides rigorous, empirical answers to every subjective analytical "
        "question presented in the project scope. All findings are derived directly from the audited dataset of 62,204 "
        "Spotify records after resolving 78 exact duplicates and 35 API-corrupted sentinel rows. "
        "Each section bridges academic descriptive statistics with operational production decisions for record producers, "
        "mixing engineers, and music strategists seeking to optimize track architecture for streaming popularity."
    )
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 1: UNIVARIATE ANALYSIS
    # ---------------------------------------------------------
    story.append(Paragraph("1. Univariate Analysis: Audio & Demographic Profiling", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    q1_1 = (
        "<b>Q1.1 Popularity Distribution:</b> The popularity score (0–100) exhibits a heavy right-skewed, zero-inflated "
        "distribution with a mean of <b>15.36</b>, standard deviation of <b>18.63</b>, and a median of only <b>7.00</b> (skewness = +1.23). "
        "Crucially, <b>28.41% (17,672 tracks)</b> possess a popularity score of exactly 0.0, indicating a massive long-tail of unpromoted, "
        "dormant, or freshly ingested music. The interquartile range (IQR) spans 26.0 points (Q1 = 0.0, Q3 = 26.0). Only <b>6.77%</b> "
        "of tracks achieve high mainstream traction exceeding 50.0 points, and the maximum observed score is 93.0."
    )
    story.append(Paragraph(q1_1, body_style))

    q1_2 = (
        "<b>Q1.2 Duration (Song Length) Typical Range:</b> Track length averages <b>242,705 ms (~4.05 minutes)</b> with a median of "
        "<b>236,379 ms (~3.94 minutes)</b> and a standard deviation of 1.88 minutes. The middle 50% (IQR) of music lies tightly "
        "between <b>3.21 minutes (192,500 ms)</b> and <b>4.77 minutes (286,240 ms)</b>. Extreme outliers range from 0.17 minutes (10 seconds, "
        "intro skits) to 76.36 minutes (unabridged audiobooks miscataloged as albums). Studio radio cuts concentrate between 3.0 and 4.0 minutes."
    )
    story.append(Paragraph(q1_2, body_style))

    q1_3 = (
        "<b>Q1.3 Musical Key Distribution:</b> The most frequent musical key is <b>C Major/Minor (8,101 tracks, 13.0%)</b>, followed by "
        "<b>G (6,956, 11.2%)</b>, <b>D (6,832, 11.0%)</b>, <b>F (6,411, 10.3%)</b>, and <b>A (5,862, 9.4%)</b>. The least common keys "
        "are D#/Eb (1,636 tracks, 2.6%) and F#/Gb (3,655 tracks, 5.9%). Western popular songwriting heavily prioritizes natural keys "
        "(C, G, D) due to standard guitar and keyboard fingerings."
    )
    story.append(Paragraph(q1_3, body_style))

    q1_4 = (
        "<b>Q1.4 Tempo Distribution:</b> Tempo displays a classic symmetric bell curve centered at a mean and median of <b>117.99 BPM</b> "
        "(standard deviation = 28.37 BPM). The distribution spans from 0.0 BPM (spoken tracks) to 240.0 BPM. Over 65% of all tracks fall "
        "between 95 and 135 BPM, capturing the universal physiological walking/heartbeat tempo standard for dance and commercial pop."
    )
    story.append(Paragraph(q1_4, body_style))

    q1_5 = (
        "<b>Q1.5 Acousticness Profile:</b> The dataset distinctly leans electronic and amplified. Mean acousticness is <b>0.363</b> "
        "(median = 0.286). Only <b>33.83%</b> of tracks have acousticness > 0.50, while <b>66.17%</b> rely on electric guitars, synthesizers, "
        "and programmed drum sequencing."
    )
    story.append(Paragraph(q1_5, body_style))

    q1_6 = (
        "<b>Q1.6 Loudness Levels (dB):</b> After eliminating corrupted -100,000 dB sentinel values, loudness ranges from <b>-60.00 dB</b> to "
        "<b>+1.23 dB</b>, with a mean of <b>-8.95 dB</b>, median of <b>-7.50 dB</b>, and standard deviation of 5.33 dB. The interquartile range "
        "spans from -10.72 dB to -5.45 dB. Modern masters concentrate tightly between -7 dB and -5 dB."
    )
    story.append(Paragraph(q1_6, body_style))

    q1_7 = (
        "<b>Q1.7 Danceability Distribution:</b> The dataset is heavily dance-oriented: mean danceability is <b>0.598</b>, median is <b>0.631</b>, "
        "and <b>74.60%</b> of tracks score above 0.50. High danceability (> 0.70) represents 31.2% of the catalog."
    )
    story.append(Paragraph(q1_7, body_style))

    q1_8 = (
        "<b>Q1.8 Energy Levels:</b> Tracks strongly favor energetic production: mean energy is <b>0.603</b>, median is <b>0.639</b>, and "
        "<b>68.45%</b> of tracks register above 0.50. The modal energy bin is <b>[0.80, 0.90]</b> containing 9,594 tracks (15.4%)."
    )
    story.append(Paragraph(q1_8, body_style))

    q1_9 = (
        "<b>Q1.9 Time Signature Prevalence:</b> Quadruple meter (<b>4/4 time</b>) overwhelmingly dominates the industry, accounting for "
        "<b>85.62% (53,260 tracks)</b>. Triple meter (3/4 time, waltz/ballad) accounts for 11.36% (7,065 tracks), followed by 5/4 meter (1.61%), "
        "and 1/4 meter (1.38%)."
    )
    story.append(Paragraph(q1_9, body_style))

    q1_10 = (
        "<b>Q1.10 Speechiness Distribution:</b> Speechiness is strongly right-skewed with a median of <b>0.049</b> and mean of <b>0.088</b>. "
        "Over <b>96.68%</b> of tracks fall below 0.33, confirming musical compositions with sung lyrics. Values > 0.66 (rap/spoken audio) represent < 1.5%."
    )
    story.append(Paragraph(q1_10, body_style))

    q1_11 = (
        "<b>Q1.11 Valence (Emotional Mood):</b> Valence is virtually perfectly balanced across the catalog: mean = <b>0.496</b>, median = <b>0.508</b>, "
        "and skewness = -0.122. There is an even spread between cheerful/euphoric music and melancholic/somber songwriting."
    )
    story.append(Paragraph(q1_11, body_style))

    q1_12 = (
        "<b>Q1.12 Instrumentalness (Vocals vs. Instrumental):</b> Overwhelmingly vocal: <b>79.38%</b> of tracks have instrumentalness < 0.10 "
        "(median = 0.000). True instrumentals (score > 0.50) represent only 12.8% of records."
    )
    story.append(Paragraph(q1_12, body_style))

    q1_13 = (
        "<b>Q1.13 Liveness (Studio vs. Concert):</b> <b>98.01%</b> of tracks have liveness < 0.80 (median = 0.125, mean = 0.195), "
        "demonstrating that the dataset reflects pristine studio-produced masters rather than live recordings."
    )
    story.append(Paragraph(q1_13, body_style))

    q1_14 = (
        "<b>Q1.14 Mode Distribution:</b> Major modality represents <b>58.7% (36,511 tracks)</b>, while Minor modality represents "
        "<b>41.3% (25,693 tracks)</b>, reflecting a 1.42:1 ratio favoring major tonalities."
    )
    story.append(Paragraph(q1_14, body_style))

    q1_15 = (
        "<b>Q1.15 Quartiles & Medians:</b> Popularity: Q1 = 0.0, Median = 7.0, Q3 = 26.0 (IQR = 26.0). "
        "Duration: Q1 = 3.21 min (192,500 ms), Median = 3.94 min (236,379 ms), Q3 = 4.77 min (286,240 ms) (IQR = 1.56 min)."
    )
    story.append(Paragraph(q1_15, body_style))

    q1_16 = (
        "<b>Q1.16 Modal Energy Level:</b> The modal decile for energy is the <b>[0.80, 0.90] interval</b> with 9,594 songs, followed closely "
        "by [0.70, 0.80] with 9,521 songs, proving that driving, high-energy mixing is the industry standard."
    )
    story.append(Paragraph(q1_16, body_style))

    q1_17 = (
        "<b>Q1.17 Language Breakdown:</b> English dominates with <b>23,366 tracks (37.6%)</b>, followed by Unknown/Instrumental (13,005, 20.9%), "
        "Tamil (12,604, 20.3%), Korean (6,887, 11.1%), Hindi (5,739, 9.2%), Telugu (321, 0.5%), and Malayalam (282, 0.5%)."
    )
    story.append(Paragraph(q1_17, body_style))
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # SECTION 2: BIVARIATE ANALYSIS
    # ---------------------------------------------------------
    story.append(Paragraph("2. Bivariate Analysis: Correlating Audio Features with Popularity", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    q2_text = (
        "We evaluated linear (Pearson <i>r</i>) and monotonic rank (Spearman <i>&rho;</i>) correlations against track popularity:<br/>"
        "• <b>Loudness vs. Popularity:</b> <b>r = +0.2012 (p < 10<sup>-300</sup>)</b>, Spearman &rho; = +0.2040. Loudness is the single strongest "
        "positive predictor of streaming popularity. Louder mixes are perceived as more impactful on mobile devices and earbuds.<br/>"
        "• <b>Energy vs. Popularity:</b> <b>r = +0.1474 (p < 10<sup>-298</sup>)</b>, Spearman &rho; = +0.1314. High-energy tracks achieve consistently higher popularity.<br/>"
        "• <b>Acousticness vs. Popularity:</b> <b>r = -0.1384 (p < 10<sup>-262</sup>)</b>. Strongest negative predictor; organic/acoustic songs face commercial headwinds.<br/>"
        "• <b>Instrumentalness vs. Popularity:</b> <b>r = -0.1271 (p < 10<sup>-221</sup>)</b>. Strong negative correlation; lack of human vocals heavily penalizes streaming reach.<br/>"
        "• <b>Duration vs. Popularity:</b> <b>r = -0.0404 (p = 6.13 &times; 10<sup>-24</sup>)</b>. Shorter tracks show slightly higher popularity due to replay loops and skip mitigation.<br/>"
        "• <b>Danceability vs. Popularity:</b> <b>r = +0.0421 (p = 9.21 &times; 10<sup>-26</sup>)</b>. Weak positive linear correlation across the full catalog, though top hits require a minimum 0.60 floor.<br/>"
        "• <b>Valence vs. Popularity:</b> <b>r = +0.0092 (p = 0.022)</b>. Statistically near zero. Listeners stream melancholic/sad songs as enthusiastically as joyful anthems.<br/>"
        "• <b>Liveness vs. Popularity:</b> <b>r = -0.0124 (p = 0.002)</b>. Studio recordings are slightly preferred over live concert takes.<br/>"
        "• <b>Tempo vs. Popularity:</b> <b>r = +0.0278 (p = 4.11 &times; 10<sup>-12</sup>)</b>. Weak positive correlation favoring moderate-to-fast tempos around 120–128 BPM.<br/>"
        "• <b>Language vs. Popularity:</b> <b>Korean leads all languages</b> with a mean popularity of <b>27.56</b> (median 26.0), followed by Hindi (18.19), "
        "English (14.77), Telugu (14.32), Tamil (11.92), and Malayalam (7.32). K-Pop and Hindi demonstrate phenomenal per-track streaming engagement.<br/>"
        "• <b>Key and Mode vs. Popularity:</b> Minor mode tracks average slightly higher popularity (<b>15.68</b>) than Major mode tracks (<b>15.14</b>), "
        "reflecting contemporary taste for minor-key moods. Top keys are D#/Eb (mean 16.40) and C#/Db (mean 16.01).<br/>"
        "• <b>Time Signature vs. Popularity:</b> 4/4 meter achieves highest average popularity (<b>15.95</b>), significantly outperforming 3/4 (12.20), "
        "5/4 (11.38), and 1/4 (9.62)."
    )
    story.append(Paragraph(q2_text, body_style))
    story.append(Spacer(1, 10))

    # Add Summary Table for Bivariate Correlations
    table_data = [
        [Paragraph("<b>Feature</b>", table_header_style), 
         Paragraph("<b>Pearson r</b>", table_header_style), 
         Paragraph("<b>p-value</b>", table_header_style), 
         Paragraph("<b>Spearman &rho;</b>", table_header_style), 
         Paragraph("<b>Engineering Takeaway</b>", table_header_style)],
        [Paragraph("Loudness (dB)", table_cell_style), Paragraph("+0.2012", table_cell_style), Paragraph("< 10<sup>-300</sup>", table_cell_style), Paragraph("+0.2040", table_cell_style), Paragraph("Master competitively (-7.5 to -6 dB RMS)", table_cell_style)],
        [Paragraph("Energy", table_cell_style), Paragraph("+0.1474", table_cell_style), Paragraph("< 10<sup>-298</sup>", table_cell_style), Paragraph("+0.1314", table_cell_style), Paragraph("Inject driving percussive/synth energy", table_cell_style)],
        [Paragraph("Acousticness", table_cell_style), Paragraph("-0.1384", table_cell_style), Paragraph("< 10<sup>-262</sup>", table_cell_style), Paragraph("-0.1200", table_cell_style), Paragraph("Avoid sparse unamplified arrangements for singles", table_cell_style)],
        [Paragraph("Instrumentalness", table_cell_style), Paragraph("-0.1271", table_cell_style), Paragraph("< 10<sup>-221</sup>", table_cell_style), Paragraph("-0.0893", table_cell_style), Paragraph("Vocal hook is mandatory for commercial reach", table_cell_style)],
        [Paragraph("Duration (ms)", table_cell_style), Paragraph("-0.0404", table_cell_style), Paragraph("6.13 &times; 10<sup>-24</sup>", table_cell_style), Paragraph("-0.0547", table_cell_style), Paragraph("Trim arrangement to 3.0–3.8 minutes", table_cell_style)],
        [Paragraph("Danceability", table_cell_style), Paragraph("+0.0421", table_cell_style), Paragraph("9.21 &times; 10<sup>-26</sup>", table_cell_style), Paragraph("-0.0150", table_cell_style), Paragraph("Maintain steady beat stability (> 0.60)", table_cell_style)],
        [Paragraph("Valence", table_cell_style), Paragraph("+0.0092", table_cell_style), Paragraph("0.0225", table_cell_style), Paragraph("-0.0322", table_cell_style), Paragraph("Both sad and euphoric songs achieve hits", table_cell_style)]
    ]
    t = Table(table_data, colWidths=[90, 60, 65, 75, 214])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 3: MULTIVARIATE ANALYSIS
    # ---------------------------------------------------------
    story.append(Paragraph("3. Multivariate Analysis: Decoding the 'Hit Recipe'", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    q3_text = (
        "<b>3.1 Hit Quadrant Feature Alignment (Top 25% Hits vs. Bottom 75%):</b><br/>"
        "Tracks in the top 25% popularity quartile (popularity &ge; 26.0) exhibit distinct multidimensional sonic shifts:<br/>"
        "• <b>Energy:</b> 0.660 (Top 25%) vs. 0.584 (Bottom 75%) — <b>+13.0% higher energy</b>.<br/>"
        "• <b>Loudness:</b> -7.25 dB vs. -9.53 dB — <b>+2.28 dB louder</b> and more cohesive.<br/>"
        "• <b>Acousticness:</b> 0.297 vs. 0.386 — <b>-23.1% lower acousticness</b> (modern electronic mastering).<br/>"
        "• <b>Instrumentalness:</b> 0.080 vs. 0.169 — <b>-52.7% reduction</b>; mainstream hits are almost exclusively vocal-driven.<br/>"
        "• <b>Duration:</b> 3.94 min vs. 4.08 min — hits are tighter and more concise.<br/><br/>"
        "<b>3.2 Popular Mix Recipe by Language:</b><br/>"
        "• <i>Korean (K-Pop):</i> Highest loudness (-4.39 dB), highest energy (0.772), danceability 0.656, tempo 123.2 BPM. K-Pop is the most "
        "densely produced, highly compressed, and rhythmically intense segment in global streaming.<br/>"
        "• <i>Hindi / Bollywood:</i> Loudness -6.95 dB, energy 0.650, danceability 0.597, valence 0.502, tempo 116.3 BPM.<br/>"
        "• <i>English:</i> Loudness -8.69 dB, energy 0.602, danceability 0.555, valence 0.418 (moodier emotional tone), tempo 118.1 BPM.<br/>"
        "• <i>Tamil:</i> High danceability (0.659), energy 0.654, valence 0.587 (most emotionally upbeat), loudness -7.70 dB.<br/><br/>"
        "<b>3.3 Harmonic & Meter Fingerprints:</b><br/>"
        "The top 5 musical configurations in the Top 25% Popularity quadrant are:<br/>"
        "1. <b>C Major in 4/4 meter</b> (1,329 hit tracks)<br/>"
        "2. <b>D Major in 4/4 meter</b> (1,118 hit tracks)<br/>"
        "3. <b>G Major in 4/4 meter</b> (1,099 hit tracks)<br/>"
        "4. <b>C#/Db Major in 4/4 meter</b> (980 hit tracks)<br/>"
        "5. <b>F Minor in 4/4 meter</b> (778 hit tracks)"
    )
    story.append(Paragraph(q3_text, body_style))
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 4: TIME-SERIES & TEMPORAL ANALYSIS
    # ---------------------------------------------------------
    story.append(Paragraph("4. Longitudinal Time-Series Analysis (1970–2024)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    q4_text = (
        "<b>4.1 The Loudness War:</b> Mastering loudness climbed steadily from <b>-10.21 dB</b> in the 1970s and <b>-11.27 dB</b> in the 1990s "
        "to a peak of <b>-8.52 dB</b> in the 2010s, stabilizing at <b>-8.72 dB</b> in the 2020s. While streaming platforms introduced LUFS normalization, "
        "producers maintain high RMS density to retain competitive punch through earbuds.<br/>"
        "<b>4.2 Song Duration Shrinkage:</b> Average track length peaked in the 1990s/2000s at 4.25 minutes and declined sharply in the 2010s (4.04 min) "
        "and 2020s (3.78 min). Streaming payouts trigger at 30 seconds of play, incentivizing shorter compositions (2.5–3.5 min) with rapid hooks.<br/>"
        "<b>4.3 Acousticness to Electronic Transition:</b> Acousticness fell from 0.44 in the 1970s to 0.33 in the 2010s, while synthetic energy rose "
        "from 0.54 to 0.63.<br/>"
        "<b>4.4 Emotional Valence Evolution:</b> Valence dropped from 0.56 in the 1970s and 0.54 in the 1980s to <b>0.48</b> in the 2010s and 2020s, "
        "demonstrating a cultural transition toward darker, introspective, and melancholic lyrical themes in modern music.<br/>"
        "<b>4.5 Global Linguistic Diversification:</b> Pre-2000 records were over 85% English. From 2010 onwards, non-English repertoire exploded: "
        "Korean, Tamil, and Hindi now represent over 41% of total catalog volume."
    )
    story.append(Paragraph(q4_text, body_style))
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 5: STATISTICAL HYPOTHESIS TESTING
    # ---------------------------------------------------------
    story.append(Paragraph("5. Statistical Hypothesis Testing & Empirical Verification", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    hyp_intro = (
        "We formalized 6 testable hypotheses evaluating distribution shape, acoustic parameters, song duration, "
        "and linguistic performance. All tests were executed at significance level &alpha; = 0.05:"
    )
    story.append(Paragraph(hyp_intro, body_style))
    story.append(Spacer(1, 6))

    hyp_data = [
        [Paragraph("<b>Hypothesis</b>", table_header_style), 
         Paragraph("<b>Null (H0) vs. Alt (H1)</b>", table_header_style), 
         Paragraph("<b>Statistical Test</b>", table_header_style), 
         Paragraph("<b>p-value</b>", table_header_style), 
         Paragraph("<b>Empirical Conclusion</b>", table_header_style)],
        
        [Paragraph("<b>H1: Popularity Skewness</b>", table_cell_style), 
         Paragraph("H0: Mean == Median<br/>H1: Median < Mean (Right-skew)", table_cell_style), 
         Paragraph("Wilcoxon signed-rank", table_cell_style), 
         Paragraph("< 10<sup>-300</sup>", table_cell_style), 
         Paragraph("<b>Reject H0:</b> Heavy right-skew (Mean 15.36 vs Median 7.00; 28.4% zero scores).", table_cell_style)],

        [Paragraph("<b>H2: Loudness Impact</b>", table_cell_style), 
         Paragraph("H0: r(loudness, pop) == 0<br/>H1: r(loudness, pop) > 0", table_cell_style), 
         Paragraph("Pearson Correlation", table_cell_style), 
         Paragraph("< 10<sup>-300</sup>", table_cell_style), 
         Paragraph("<b>Reject H0:</b> Highly significant positive correlation (r = +0.2012).", table_cell_style)],

        [Paragraph("<b>H3: Radio Duration Sweet Spot</b>", table_cell_style), 
         Paragraph("H0: &mu;(Radio) == &mu;(Long)<br/>H1: &mu;(Radio) > &mu;(Long)", table_cell_style), 
         Paragraph("Welch's Two-Sample t-test", table_cell_style), 
         Paragraph("2.41 &times; 10<sup>-18</sup>", table_cell_style), 
         Paragraph("<b>Reject H0:</b> Radio edits (2.5–4.0m) score 16.42 vs 13.88 for long tracks.", table_cell_style)],

        [Paragraph("<b>H4: Vocal Presence vs. Instrumental</b>", table_cell_style), 
         Paragraph("H0: &mu;(Vocal) == &mu;(Inst)<br/>H1: &mu;(Vocal) > &mu;(Inst)", table_cell_style), 
         Paragraph("Welch's Two-Sample t-test", table_cell_style), 
         Paragraph("< 10<sup>-100</sup>", table_cell_style), 
         Paragraph("<b>Reject H0:</b> Vocal tracks average 16.71 vs 8.92 for instrumentals (-46.6%).", table_cell_style)],

        [Paragraph("<b>H5: Language Performance (Korean vs. English)</b>", table_cell_style), 
         Paragraph("H0: &mu;(Korean) == &mu;(English)<br/>H1: &mu;(Korean) > &mu;(English)", table_cell_style), 
         Paragraph("Welch's Two-Sample t-test", table_cell_style), 
         Paragraph("< 10<sup>-150</sup>", table_cell_style), 
         Paragraph("<b>Reject H0:</b> Korean music exhibits significantly higher popularity (27.56 vs 14.77).", table_cell_style)],

        [Paragraph("<b>H6: Time Signature Advantage</b>", table_cell_style), 
         Paragraph("H0: &mu;(4/4) == &mu;(Non-4/4)<br/>H1: &mu;(4/4) > &mu;(Non-4/4)", table_cell_style), 
         Paragraph("Welch's Two-Sample t-test", table_cell_style), 
         Paragraph("8.94 &times; 10<sup>-65</sup>", table_cell_style), 
         Paragraph("<b>Reject H0:</b> 4/4 meter averages 15.95 vs 11.83 for non-4/4 meters.", table_cell_style)]
    ]

    htable = Table(hyp_data, colWidths=[80, 110, 85, 65, 164])
    htable.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(htable)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 6: STRATEGIC RECOMMENDATIONS
    # ---------------------------------------------------------
    story.append(Paragraph("6. Operational Directives for Music Directors & Audio Engineers", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    recs = [
        "<b>Directive 1: Calibrate Audio Profile into the 'Energetic & Danceable' Sweet Spot</b><br/>"
        "• <i>Target Specifications:</i> Danceability &ge; 0.62, Energy &ge; 0.68, Tempo between 118 and 126 BPM in 4/4 meter.<br/>"
        "• <i>Action:</i> Center arrangements on driving kick/bass interaction and rhythm section clarity. Top 25% tracks exhibit an average "
        "energy of 0.660 (+13% over non-hits). Avoid overly sparse or unamplified arrangements for lead singles.",

        "<b>Directive 2: Master for Modern, Competitive Impact (-7.5 dB to -6.0 dB RMS)</b><br/>"
        "• <i>Target Specifications:</i> Integrated Loudness: -12 to -9 LUFS; Dynamic Range: 6–8 dB; RMS Loudness: -7.5 to -6.0 dB.<br/>"
        "• <i>Action:</i> While streaming normalization standards (-14 LUFS) govern target playback volume, tracks with denser, louder mix-buses "
        "(r = +0.201, p < 10<sup>-300</sup>) project greater punch, presence, and vocal intelligibility across earphone transducers. "
        "Utilize multi-band saturation and serial limiting to avoid transient distortion.",

        "<b>Directive 3: Structure Radio Edits at 3.0 to 3.8 Minutes to Maximize Algorithmic Lift</b><br/>"
        "• <i>Target Specifications:</i> Track length: 180 to 228 seconds (3:00 to 3:48). Intro length < 10 seconds.<br/>"
        "• <i>Action:</i> Radio edits outperform tracks exceeding 4.5 minutes by +18.3% in popularity (p = 2.41 &times; 10<sup>-18</sup>). "
        "Deliver the chorus within the first 45 seconds to suppress playlist skip rates, which algorithmically downgrade track recommendation velocity.",

        "<b>Directive 4: Prioritize Vocal Intelligibility and Front-and-Center Mix Staging</b><br/>"
        "• <i>Target Specifications:</i> Instrumentalness < 0.05. Clear vocal formant presence in the 1.5 kHz – 4.5 kHz octave.<br/>"
        "• <i>Action:</i> Instrumental compositions suffer a 46.6% popularity penalty compared to vocal songs (8.92 vs 16.71, p < 10<sup>-100</sup>). "
        "Carve spectral space in competing synthesizers and guitars using sidechain dynamic EQ to keep lead vocals prominent.",

        "<b>Directive 5: Leverage International Market Dynamism (K-Pop & Indian Curation)</b><br/>"
        "• <i>Target Specifications:</i> Explore multilingual hooks, transnational features, and dense K-Pop-style arrangement dynamics.<br/>"
        "• <i>Action:</i> Korean records boast an average popularity of 27.56 (almost double the English average of 14.77). "
        "Incorporating high-energy syncopation and cross-market vocal features provides an immediate multiplier for global playlist traction."
    ]

    for rec in recs:
        story.append(Paragraph(rec, body_style))
        story.append(Spacer(1, 5))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {pdf_path}")

if __name__ == '__main__':
    build_pdf()

