import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# ==========================================
# 1. CONFIGURATION (Edit everything here)
# ==========================================
class Config:
    OUTPUT_FILE = "Wedding_Bingo_2026.pdf"
    NUM_CARDS = 44
    GRID_SIZE = 3
    
    # --- Fonts ---
    TITLE_FONT_FILE = "HolidayFree.ttf"
    BODY_FONT_FILE = "times.ttf"
    TITLE_FONT_NAME = 'HolidayFont'
    BODY_FONT_NAME = 'BodyFont'
    
    # --- Sizes ---
    TITLE_SIZE = 72
    SUBTITLE_SIZE = 28
    INSTR_FONT_SIZE = 13
    GRID_TEXT_SIZE = 15
    
    # --- Layout & Spacing ---
    SQUARE_SIDE = 6.0 * cm  
    SQUARE_PADDING = 0.5 * cm  # Padding inside the box
    LINE_SPACING_INSTR = 0.75 * cm  # Gap between instruction lines
    LINE_SPACING_GRID = 1.2  # Multiplier for grid text height
    
    # --- Y-Positions (Vertical Placement) ---
    TITLE_Y = 26.5 * cm
    SUBTITLE_Y = 24.5 * cm
    INSTR_START_Y = 22.5 * cm
    
    GAP_BELOW_INSTR = 1.5 * cm 
    
    INSTRUCTIONS = [
        "ATRODI KATRAM LAUCIŅAM ATBILSTOŠU VIESI UN LŪDZ TAJĀ PARAKSTĪTIES.",
        "KATRS CILVĒKS TAVĀ KARTĪTĒ DRĪKST PARAKSTĪTIES TIKAI VIENU REIZI.",
        "UZVAR TAS, KURŠ PIRMAIS AIZPILDA VISU TABULU!"
    ]

# ==========================================
# 2. DATA
# ==========================================
PROMPTS = [
    "Ir pazīstams ar Agnesi kopš bērnudārza vai skolas",
    "Ir pazīstams ar Rihardu kopš bērnudārza vai skolas",
    "Ir ceļojis vairāk nekā 100 km, lai būtu šeit",
    "Māk spēlēt kādu mūzikas instrumentu",
    "Ir suņa saimnieks",
    "Runā vismaz trīs valodās",
    "Ir laulībā vairāk nekā 5 gadus",
    "Mājās ir vismaz viens mājdzīvnieks",
    "Ir no tās pašas pilsētas, kur piedzimis tu pats",
    "Ir izlasījis grāmatu pēdējā mēneša laikā",
    "Ir Agneses māsīca",
    "Ir Agneses māsa",
    "Nokārtojis autovadītāja tiesības ar pirmo reizi",
    "Ir pabijis vismaz 10 dažādās valstīs",
    "Šodien izdzēra vismaz 2 kafijas krūzes",
    "Prot pagatavot biešu zupu",
    "Ir tāds pats apavu izmērs kā tev",
    "Ir dzimis tajā pašā mēnesī, kurā tu",
    "Strādā tajā pašā nozarē vai profesijā, kurā tu",
    "Ir domājis skriet maratonu",
    "Šobrīd mugurā ir, kāds melns apģērba gabals",
    "Ir jaunāks par Rihardu",
    "Atbrauca ar zilu automašīnu",
    "Nekad nav redzējis nevienu 'Zvaigžņu karu' filmu",
    "Ir kaķa saimnieks",
    "Pēdējā gada laikā ir iemācījies jaunu prasmi",
    "Ir gājis dejošanas nodarbībās",
    "Ir mācījies vienā klasē ar Agnesi",
    "Prot pateikt 'Jā' piecās valodās",
    "Ir vecākais bērns savā ģimenē",
    "Ir mācījies ārzemēs",
    "Ir izceļojis ārpus Latvijas 2026. gadā",
    "Prot dejot tautas dejas vai valsi",
    "Ir šajā pasākumā uzņēmis vismaz 5 bildes",
    "Nav dzēris nevienu alkoholisku dzērienu šovakar",
    "Nēsā brilles vai kontaktlēcas",
    "Ir kādreiz dziedājis korī",
    "Prot uztaisīt 'tiltiņu' vai špagatu",
    "Ir noskatījies vismaz 3 seriālus pēdējā pusgada laikā",
    "Uzvārdā ir vismaz 8 burti",
    "Ir bijis uz koncertu pēdējo 6 mēnešu laikā",
    "Ir bijis uz teātra izrādi pēdējo 6 mēnešu laikā",
    "Apmeklējis sporta zāli pēdējās nedēļas laikā",
    "Ir vismaz par 10 gadiem vecāks par Rihardu",
    "Ir redzējis visas 'Harija Potera' filmas",
    "Šovakar ir uzvilcis kaut ko pilnīgi jaunu",
    "Ir lielāks telefona akumulatora uzlādes līmenis nekā tev",
    "Ir kādreiz dzīvē uzstājies uz skatuves",
    "Ir piedalījies Dziesmu un deju svētkos",
    "Vārdā ir vismaz 3 patskaņi (piem. A, E, I, O, U)",
    "Prot pagatavot vismaz 3 dažādus kokteiļus",
    "Ir redzējis filmu 'Limuzīns Jāņu nakts krāsā'",
    "Ir bijis uz kāzām ārzemēs",
    "Ir ieguvis bakalaura grādu",
    "Mājās pie sienas ir glezna",
    "Ir piedalījies televīzijas raidījumā vai intervijā",
    "Ir vismaz divu Apple produktu īpašnieks"
]

# ==========================================
# 3. UTILITIES
# ==========================================
def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont(Config.TITLE_FONT_NAME, Config.TITLE_FONT_FILE))
        pdfmetrics.registerFont(TTFont(Config.BODY_FONT_NAME, Config.BODY_FONT_FILE))
        return True
    except Exception as e:
        print(f"Error loading fonts: {e}")
        return False

def wrap_text(text, font_name, font_size, max_width, c):
    words = text.split()
    lines, current_line = [], []
    for word in words:
        current_line.append(word)
        if c.stringWidth(" ".join(current_line), font_name, font_size) < max_width:
            continue
        else:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# ==========================================
# 4. DRAWING LOGIC
# ==========================================
def draw_card(c, prompts):
    width, height = A4
    
    # 1. Titles
    c.setFillColor(colors.black)
    c.setFont(Config.TITLE_FONT_NAME, Config.TITLE_SIZE)
    c.drawCentredString(width/2, Config.TITLE_Y, "atrodi viesi")
    
    c.setFont(Config.BODY_FONT_NAME, Config.SUBTITLE_SIZE)
    c.drawCentredString(width/2, Config.SUBTITLE_Y, "K Ā Z U  B I N G O")
    
    # 2. Instructions
    c.setFont(Config.BODY_FONT_NAME, Config.INSTR_FONT_SIZE)
    y_current = Config.INSTR_START_Y
    for text in Config.INSTRUCTIONS:
        c.drawCentredString(width/2, y_current, text)
        y_current -= Config.LINE_SPACING_INSTR

    # 3. Calculate Grid Start
    last_instr_y = y_current + Config.LINE_SPACING_INSTR
    start_y = last_instr_y - Config.GAP_BELOW_INSTR
    
    total_grid_w = Config.GRID_SIZE * Config.SQUARE_SIDE
    start_x = (width - total_grid_w) / 2
    
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)

    for i in range(Config.GRID_SIZE):
        for j in range(Config.GRID_SIZE):
            x = start_x + j * Config.SQUARE_SIDE
            y = start_y - (i + 1) * Config.SQUARE_SIDE
            
            c.rect(x, y, Config.SQUARE_SIDE, Config.SQUARE_SIDE)
            
            # --- UPPERCASE TRANSFORMATION ---
            raw_text = prompts[i * Config.GRID_SIZE + j]
            p_text = raw_text.upper() 
            
            lines = wrap_text(p_text, Config.BODY_FONT_NAME, Config.GRID_TEXT_SIZE, Config.SQUARE_SIDE - Config.SQUARE_PADDING*2, c)
            
            # Vertical center logic
            line_h = Config.GRID_TEXT_SIZE * Config.LINE_SPACING_GRID
            total_h = len(lines) * line_h
            current_text_y = y + (Config.SQUARE_SIDE/2) + (total_h/2) - line_h
            
            c.setFont(Config.BODY_FONT_NAME, Config.GRID_TEXT_SIZE)
            for line in lines:
                c.drawCentredString(x + Config.SQUARE_SIDE/2, current_text_y, line)
                current_text_y -= line_h

# ==========================================
# 5. EXECUTION
# ==========================================
def main():
    if not register_fonts():
        return
    c = canvas.Canvas(Config.OUTPUT_FILE, pagesize=A4)
    print(f"Creating {Config.NUM_CARDS} cards...")
    for _ in range(Config.NUM_CARDS):
        selected = random.sample(PROMPTS, Config.GRID_SIZE**2)
        draw_card(c, selected)
        c.showPage()
    c.save()
    print(f"Success! {Config.OUTPUT_FILE} created.")

if __name__ == "__main__":
    main()