# -*- coding: utf-8 -*-
"""Inhoud van Tandartspraktijk Badhuisplein (Nederlands).

Teksten zijn herschreven op basis van de oude website en aangevuld voor
vindbaarheid. Feiten (team, tijden, telefoonnummers) komen van praktijkbadhuisplein.nl.
"""

TEAM = {
    "alvaro":     ("Alvaro Soler", "Tandarts voor implantologie en orthodontie", "tandarts"),
    "kinan":      ("Kinan Khalil", "Tandarts voor implantologie", "tandarts"),
    "ana":        ("Ana Recas", "Tandarts voor esthetiek en implantologie", "tandarts"),
    "itschi":     ("Itschi Okpara", "Tandarts", "tandarts"),
    "roos":       ("Roos", "Ortho-, paro- en preventieassistente", "mondzorg"),
    "anja":       ("Anja", "Preventieassistente", "mondzorg"),
    "maaike":     ("Maaike", "Ortho- en preventieassistente", "mondzorg"),
    "stefanie":   ("Stefanie", "Ortho- en preventieassistente", "mondzorg"),
    "madee":      ("Madée", "Preventieassistente", "mondzorg"),
    "rozemarijn": ("Rozemarijn", "Preventieassistente", "mondzorg"),
    "mirjam":     ("Mirjam", "Tandartsassistente", "mondzorg"),
    "sigita":     ("Sigita", "KPT-assistente", "mondzorg"),
    "hala":       ("Hala", "Stagiaire", "mondzorg"),
    "serge":      ("Serge", "Tandprotheticus", "prothetiek"),
    "ferdy":      ("Ferdy", "Tandtechnieker", "prothetiek"),
    "lucette":    ("Lucette", "Praktijkmanager", "balie"),
    "henriette":  ("Henriëtte", "Baliemedewerkster", "balie"),
    "louise":     ("Louise", "Baliemedewerkster", "balie"),
    "veerle":     ("Veerle", "Baliemedewerkster", "balie"),
}

# slug, menunaam, korte omschrijving, icoon
TREATMENTS = [
    ("esthetische-behandelingen", "Esthetisch", "Kleur, stand of vorm verbeteren met facings, kronen en witte vullingen.", "esthetisch"),
    ("bleken", "Bleken", "Enkele tinten lichter, nadat de tandarts uw gebit heeft bekeken.", "bleken"),
    ("implantaten", "Implantaten", "Kroon, brug of klikgebit op implantaten, gepland met onze CBCT-scan.", "implantaten"),
    ("kronen-en-bruggen", "Kronen en bruggen", "Na een scan is een kroon meestal dezelfde dag klaar.", "kronen"),
    ("protheses", "Protheses", "Kunstgebit, frame of plaatje, met reparaties in eigen laboratorium.", "protheses"),
    ("othodontie-en-invisalign", "Orthodontie & Invisalign", "Invisalign, Spark of brackets, met een gratis intake.", "orthodontie"),
    ("vullingen", "Vullingen", "Altijd wit composiet; u kiest zelf of u verdoving wilt.", "vullingen"),
    ("extractie-trekken", "Extractie (trekken)", "Goed verdoofd, met duidelijk advies voor daarna.", "extractie"),
    ("wortelkanaalbehandeling", "Wortelkanaalbehandeling", "De ontsteking stoppen en uw eigen tand behouden.", "wortelkanaal"),
    ("preventie-en-mondhygiene", "Preventie en mondhygiëne", "Gebitsreiniging en persoonlijk advies van ons preventieteam.", "preventie"),
]

T = {}

T["esthetische-behandelingen"] = dict(
    title="Esthetische tandheelkunde Hardenberg | Facings en bleken",
    desc="De kleur, stand of vorm van uw tanden verbeteren in Hardenberg? Facings, kronen, witte vullingen of bleken, met een plan en begroting op maat.",
    h1='Esthetische tandheelkunde in <em class="g">Hardenberg</em>',
    lead="Wilt u de kleur, stand of vorm van uw tanden verbeteren? We vertellen u graag wat er mogelijk is en stellen een behandelplan en begroting op die passen bij uw wensen en budget.",
    img="esthetisch.webp", img_alt="Twee assistentes van de praktijk bij een jonge patiënte in de behandelstoel", img_pos="60% 40%",
    procedure="Esthetische tandheelkunde",
    who=["ana"],
    body="""
<h2>Wat kunnen we voor u doen?</h2>
<p>Een verkleurde voortand, een afgebroken hoekje of een oude vulling die opvalt: er is meestal meer mogelijk dan u denkt. We kijken eerst of uw gebit en tandvlees gezond zijn. Pas daarna bespreken we het uiterlijk, want een mooi resultaat moet ook blijven zitten.</p>
<ul class="types">
  <li><b>Kronen en brugwerk</b><span>Van keramiek, voor tanden die zwaar beschadigd zijn of ontbreken.</span></li>
  <li><b>Facings</b><span>Dunne schildjes van keramiek of composiet, bijvoorbeeld voor scheve of afgebroken tanden.</span></li>
  <li><b>Tandkleurige vullingen</b><span>Al onze vullingen maken we van wit composiet.</span></li>
  <li><b>Bleken</b><span>Uw tanden enkele tinten lichter, als uw gebit daarvoor geschikt is.</span></li>
</ul>
<h2>Van wens naar behandelplan</h2>
<ol>
  <li><b>U vertelt wat u wilt.</b> De tandarts onderzoekt uw gebit en legt uit wat er kan en wat er verstandig is.</li>
  <li><b>U krijgt een plan met begroting.</b> Afgestemd op uw wensen en uw budget, zodat u weet waar u aan toe bent.</li>
  <li><b>We voeren het plan uit.</b> Kronen maken we na een scan vaak op dezelfde dag; ander werk komt uit ons eigen tandtechnisch laboratorium.</li>
</ol>
<div class="note"><p><b>Vergoeding.</b> Esthetische behandelingen voor volwassenen vallen meestal niet onder de basisverzekering. Een aanvullende tandartsverzekering vergoedt soms een deel. Lees meer over <a href="{u:homepage/betalen-en-vergoedingen/}">verzekering en vergoedingen</a>.</p></div>
""",
    faq=[
        ("Wat is het verschil tussen een facing en een kroon?", "Een facing is een dun schildje op de voorkant van de tand en verbetert vooral het uiterlijk. Een kroon past als een kapje over de hele afgeslepen tand en is bedoeld voor tanden die verzwakt of zwaar beschadigd zijn."),
        ("Verkleuren facings door koffie of rode wijn?", "Keramische facings zijn kleurvast: koffie, thee en rode wijn hebben geen invloed op de kleur. Composiet kan na verloop van tijd wel wat verkleuren."),
        ("Weet ik vooraf wat het kost?", "Ja. U krijgt een behandelplan met begroting. Voor behandelingen boven de € 250 kunt u om een schriftelijke begroting vragen."),
    ],
    related=["bleken", "kronen-en-bruggen", "othodontie-en-invisalign"],
)

T["bleken"] = dict(
    title="Tanden bleken Hardenberg | Veilig bij de tandarts",
    desc="Tanden bleken in Hardenberg? Bij Tandartspraktijk Badhuisplein kijkt de tandarts eerst of het kan en wat bij u past. Lees hoe het werkt en wat u kunt verwachten.",
    h1='Tanden <em class="g">bleken</em> bij de tandarts',
    lead="Tanden worden met de jaren donkerder. Bleken kan ze enkele tinten lichter maken, maar het kan niet altijd. Daarom bespreekt u uw wensen eerst met de tandarts.",
    img="bleken.webp", img_alt="Assistente van de praktijk in gesprek met een jonge patiënte in de behandelstoel", img_pos="62% 40%",
    procedure="Tanden bleken",
    who=["ana"],
    body="""
<h2>Waarom worden tanden donkerder?</h2>
<p>Dat tanden en kiezen verkleuren is normaal. Roken, koffie, thee, wijn, frisdrank en vruchtensap laten kleurstoffen achter. Bij het ouder worden ontstaan bovendien kleine barstjes in het glazuur, waardoor die kleurstoffen nog makkelijker in de tand trekken.</p>
<h2>Eerst kijken of het kan</h2>
<p>Bleken kan in veel gevallen, maar zeker niet altijd. De tandarts kijkt eerst naar uw gebit: zijn er gaatjes, is het tandvlees gezond en waar zitten vullingen of kronen? Die bleken namelijk niet mee. Daarna hoort u of bleken bij u past en welke aanpak we adviseren.</p>
<div class="note"><p><b>Waarom via de tandarts?</b> Bleekmiddelen met een werkzame concentratie mogen in Nederland alleen door of onder toezicht van een tandarts worden gebruikt. Zo weet u dat het veilig gebeurt.</p></div>
<h2>Na het bleken</h2>
<ul>
  <li>Uw tanden kunnen een paar dagen gevoeliger zijn voor warm en koud. Dat trekt vanzelf weg.</li>
  <li>Met minder koffie, thee, rode wijn en roken blijft het resultaat langer mooi.</li>
  <li>Goed poetsen en <a href="{u:behandelingen/preventie-en-mondhygiene/}">gebitsreiniging</a> houden verkleuring langer weg.</li>
</ul>
""",
    faq=[
        ("Is bleken schadelijk voor mijn tanden?", "Onder begeleiding van de tandarts niet. Vooraf wordt gecontroleerd of uw gebit gezond is. Tijdelijke gevoeligheid kan voorkomen."),
        ("Hoe lang blijven mijn tanden lichter?", "Dat verschilt per persoon. Wie weinig koffie, thee of wijn drinkt en niet rookt, houdt het resultaat het langst."),
        ("Worden vullingen en kronen ook lichter?", "Nee, alleen natuurlijk tandweefsel bleekt. Zitten er vullingen of kronen in het zicht, dan bespreken we vooraf wat dat betekent voor het resultaat."),
        ("Wordt bleken vergoed?", "Bleken is een cosmetische behandeling en wordt meestal niet vergoed. U kunt vooraf een begroting krijgen."),
    ],
    related=["esthetische-behandelingen", "preventie-en-mondhygiene", "kronen-en-bruggen"],
)

T["implantaten"] = dict(
    title="Tandimplantaten Hardenberg | Implantoloog en 3D CBCT-scan",
    desc="Implantaat nodig in Hardenberg? Kroon, brug of klikgebit op implantaten, gepland met onze eigen CBCT-scan en in overleg met de tandprotheticus.",
    h1='Tandimplantaten in <em class="g">Hardenberg</em>',
    lead="Een implantaat is een kunstwortel van titanium die in het kaakbot wordt geplaatst. Daarop komt een kroon, een brug of een prothese. Tandartsen, implantoloog en tandprothetici stemmen de behandeling samen af.",
    img="team/alvaro.webp", img_alt="Alvaro Soler, tandarts voor implantologie en orthodontie bij Tandartspraktijk Badhuisplein",
    procedure="Tandimplantaat",
    who=["alvaro", "kinan", "ana"],
    body="""
<h2>Drie manieren om implantaten te gebruiken</h2>
<ul class="types">
  <li><b>Kroon op implantaat</b><span>Mist u één tand of kies? Het implantaat krijgt een vastgeschroefde of gelijmde kroon, en de buurtanden blijven onaangeroerd.</span></li>
  <li><b>Brug op implantaten</b><span>Bij meerdere ontbrekende tanden krijgt u een vaste vervanging. Een driedelige brug kan soms op twee implantaten.</span></li>
  <li><b>Klikgebit</b><span>Slinkt het kaakbot, dan gaat een prothese los zitten. Op drukknoppen of een steg op implantaten klikt hij stevig vast.</span></li>
</ul>
<h2>Gepland met een 3D-scan</h2>
<p>De praktijk heeft een eigen <a href="{u:cbct-rontgen/}">Cone Beam CT-scanner</a>. Daarmee beoordelen we hoeveel kaakbot er is op de plek van het nieuwe implantaat en hoe eerder geplaatste implantaten ervoor staan. Voor die scan hoeft u dus niet naar een ziekenhuis.</p>
<h2>Het traject</h2>
<ol>
  <li><b>Onderzoek.</b> We bespreken uw wensen, bekijken mond en kaak en maken zo nodig een CBCT-scan.</li>
  <li><b>Plan en begroting.</b> U weet vooraf wat er gaat gebeuren en wat het kost.</li>
  <li><b>Plaatsen.</b> Het implantaat wordt onder plaatselijke verdoving in het kaakbot gezet.</li>
  <li><b>Ingroeien.</b> Het implantaat groeit in de kaak vast. Dat duurt een aantal maanden.</li>
  <li><b>Kroon, brug of prothese.</b> Daarna komt de definitieve vervanging op het implantaat.</li>
</ol>
<p>Een klikgebit wordt voor een groot deel vergoed uit de basisverzekering. Een kroon of brug op implantaten voor volwassenen meestal niet. Lees meer over <a href="{u:homepage/betalen-en-vergoedingen/}">vergoedingen</a>.</p>
""",
    faq=[
        ("Doet het plaatsen van een implantaat pijn?", "Het gebeurt onder plaatselijke verdoving, dus tijdens de behandeling voelt u geen pijn. De dagen erna kan het wat gevoelig of gezwollen zijn."),
        ("Ben ik geschikt voor een implantaat?", "Dat hangt onder meer af van de hoeveelheid kaakbot en uw algemene gezondheid. Met onze CBCT-scan kunnen we dat nauwkeurig beoordelen."),
        ("Moeten de tanden ernaast worden geslepen?", "Bij een kroon op een implantaat niet. Dat is een groot verschil met een gewone brug, waarvoor de buurtanden worden afgeslepen."),
        ("Wordt een klikgebit vergoed?", "Een klikgebit wordt voor een groot deel vergoed uit de basisverzekering. Vraag uw zorgverzekeraar naar de juiste vergoeding."),
    ],
    related=["protheses", "kronen-en-bruggen", "extractie-trekken"],
)

T["kronen-en-bruggen"] = dict(
    title="Kronen en bruggen Hardenberg | Vaak dezelfde dag geplaatst",
    desc="Kroon nodig in Hardenberg? Na een digitale scan plaatsen we een normale kroon meestal dezelfde dag. Soms maakt ons eigen lab hem in circa twee weken.",
    h1='Een kroon, vaak op <em class="g">dezelfde dag</em>',
    lead="Kronen en bruggen herstellen de vorm en functie van uw tanden en kiezen. Na het voorbereiden en een scan kan een normale kroon in de meeste gevallen aan het eind van de middag al worden geplaatst.",
    img="cadcam.webp", img_alt="Medewerker van de praktijk bij de machine die kronen op maat maakt", img_pos="62% 50%",
    procedure="Kroon- en brugwerk",
    who=["ferdy", "itschi"],
    body="""
<h2>Kroon of brug: wat is het verschil?</h2>
<p>Een <b>kroon</b> is een kapje dat precies over een afgeslepen tand of kies past, zodat die zijn vorm en functie terugkrijgt. Een <b>brug</b> vervangt één of meer ontbrekende tanden of kiezen en zit vast aan afgeslepen tanden aan weerszijden van de open ruimte, de pijlers. Ontbreken die pijlers, dan kan een <a href="{u:behandelingen/implantaten/}">brug op implantaten</a> een oplossing zijn.</p>
<h2>Hoe verloopt de behandeling?</h2>
<ol>
  <li><b>Voorbereiden.</b> De tand of kies wordt omslepen en de tandarts maakt een scan en/of afdruk van uw gebit.</li>
  <li><b>Maken.</b> Een normale kroon wordt op basis van de scan gemaakt en kan in de meeste gevallen dezelfde dag, aan het eind van de middag, worden geplaatst.</li>
  <li><b>Plaatsen.</b> In sommige gevallen maakt ons tandtechnisch laboratorium de kroon of brug. Die wordt dan circa twee weken later geplaatst.</li>
</ol>
<figure><img src="{a:assets/img/ferdy-techniek.webp}" alt="Tandtechnieker Ferdy aan het werk in het eigen tandtechnisch laboratorium" width="950" height="634" loading="lazy" decoding="async"><figcaption>Ferdy, onze tandtechnieker, in het eigen laboratorium.</figcaption></figure>
<h2>Welke materialen zijn er?</h2>
<ul class="types">
  <li><b>Keramiek</b><span>Tandkleurig en natuurgetrouw. Dankzij nieuwe technieken is de kans op breuk nagenoeg uitgesloten.</span></li>
  <li><b>Goud-keramiek</b><span>Een basis van goudlegering met een laag tandkleurig keramiek eroverheen.</span></li>
  <li><b>Goud</b><span>Zeer sterk en slijtvast. Door de kleur vooral voor kiezen achter in de mond.</span></li>
  <li><b>Inlay</b><span>Als een groot deel van de kies nog goed is, is een volledige kroon soms niet nodig. Van goud, keramiek of composiet.</span></li>
  <li><b>Facing</b><span>Een dun schildje voor de voorkant van de tand; kleurvast bij koffie, thee en rode wijn.</span></li>
  <li><b>Opbouw</b><span>Extra houvast voor de kroon of brug, met een pin vastgelijmd in het wortelkanaal.</span></li>
</ul>
""",
    faq=[
        ("Kan een kroon echt op dezelfde dag?", "Ja, een normale kroon kan in de meeste gevallen dezelfde dag aan het eind van de middag worden geplaatst. Soms is het laboratorium nodig; dan duurt het circa twee weken."),
        ("Wat kost een kroon of brug?", "De tarieven worden vastgesteld door de Nederlandse Zorgautoriteit (NZa). U kunt vooraf een begroting krijgen, boven de € 250 ook schriftelijk."),
        ("Wordt een kroon vergoed?", "Voor volwassenen niet uit de basisverzekering, wel soms deels uit een aanvullende tandartsverzekering. Ook voor kinderen tot 18 jaar vallen kronen en bruggen buiten de basisverzekering."),
    ],
    related=["implantaten", "esthetische-behandelingen", "wortelkanaalbehandeling"],
)

T["protheses"] = dict(
    title="Kunstgebit en klikgebit Hardenberg | Tandprotheticus",
    desc="Kunstgebit, frame of plaatje in Hardenberg? Onze tandprotheticus en tandtechnieker werken in hetzelfde pand. Reparaties doorgaans aan het eind van de dag klaar.",
    h1='Kunstgebit, frame of <em class="g">klikgebit</em>',
    lead="Heeft u geen of bijna geen eigen tanden meer, dan kan een prothese uitkomst bieden. Tandartsen, implantoloog en tandprothetici werken nauw samen, en reparaties gebeuren in ons eigen laboratorium.",
    img="serge-behandeling.webp", img_alt="Tandprotheticus Serge bij een patiënte in de behandelkamer", img_pos="40% 40%",
    procedure="Gebitsprothese",
    who=["serge", "ferdy"],
    body="""
<h2>Welke prothese past bij u?</h2>
<p>We maken onderscheid tussen een volledige prothese, het kunstgebit, en een gedeeltelijke of partiële prothese. Beide zijn uitneembaar. Zit een prothese los, dan kan hij op <a href="{u:behandelingen/implantaten/}">implantaten</a> worden vastgeklikt.</p>
<ul class="types">
  <li><b>Volledige prothese</b><span>Vervangt alle natuurlijke tanden en kiezen als die verloren zijn gegaan.</span></li>
  <li><b>Frameprothese</b><span>Een metalen frame met haakjes om uw eigen tanden. Sterker dan een plaatje, en daardoor dunner en kleiner.</span></li>
  <li><b>Kunststof plaatje</b><span>Relatief goedkoop maar minder duurzaam. Vaak een tijdelijke oplossing na het trekken van tanden.</span></li>
  <li><b>Klikgebit</b><span>Een prothese die via drukknoppen of een steg vastklikt op implantaten.</span></li>
</ul>
<h2>Tandprothetische Praktijk Zieck, in hetzelfde pand</h2>
<p>In ons pand op huisnummer 2 (ingang B) is Tandprothetische Praktijk Zieck gevestigd, voor het aanmeten, maken en repareren van uitneembare protheses, frames, plaatjes en protheses op implantaten. Doordat we nauw samenwerken, stemmen we behandelingen moeiteloos op elkaar af.</p>
<h2>Reparatie in eigen laboratorium</h2>
<p>Reparaties aan gebitsprotheses doen we in ons eigen laboratorium. Doorgaans is uw prothese aan het eind van de dag klaar.</p>
<ul>
  <li><b>Maandag t/m woensdag:</b> brengen vóór 12:30 uur, ophalen om 16:00 uur.</li>
  <li><b>Donderdag en vrijdag:</b> alleen noodreparaties.</li>
</ul>
<p>Bel gerust even van tevoren: <a href="tel:+31523216967">0523-216967</a>.</p>
""",
    faq=[
        ("Wat is het verschil tussen een kunstgebit en een klikgebit?", "Een gewoon kunstgebit is volledig uitneembaar. Een klikgebit klikt vast op implantaten in de kaak en biedt daardoor meer houvast en zekerheid."),
        ("Mijn prothese zit los. Wat kan ik doen?", "Door het slinken van het kaakbot kan een prothese na verloop van tijd los gaan zitten. Kom langs voor advies; soms is een klikgebit de oplossing."),
        ("Wordt een kunstgebit vergoed?", "Kunstgebitten en klikgebitten worden voor een groot deel vergoed uit de basisverzekering. Vraag uw zorgverzekeraar naar de juiste vergoeding."),
        ("Wanneer is mijn reparatie klaar?", "Brengt u de prothese maandag t/m woensdag vóór 12:30 uur, dan kunt u hem om 16:00 uur ophalen. Op donderdag en vrijdag doen we alleen noodreparaties."),
    ],
    related=["implantaten", "extractie-trekken", "kronen-en-bruggen"],
)

T["othodontie-en-invisalign"] = dict(
    title="Invisalign en beugel Hardenberg | Gratis intake orthodontie",
    desc="Rechte tanden in Hardenberg met Invisalign, Spark of brackets. Tijdens een gratis intake bij Tandartspraktijk Badhuisplein hoort u welke beugel bij u past.",
    h1='Orthodontie en <em class="g">Invisalign</em>',
    lead="Rechte tanden zijn mooi, en ook beter voor bijten, kauwen en poetsen. We werken met onzichtbare aligners van Invisalign en Spark en met brackets. Tijdens een gratis intake kijken we wat bij u past.",
    img="scan.webp", img_alt="Assistente maakt een digitale scan van het gebit van een patiënte", img_pos="45% 40%",
    procedure="Orthodontische behandeling",
    who=["alvaro", "roos", "maaike", "stefanie"],
    body="""
<h2>Drie manieren om tanden recht te zetten</h2>
<ul class="types">
  <li><b>Invisalign</b><span>Een reeks doorzichtige, uitneembare aligners, op maat gemaakt voor uw gebit.</span></li>
  <li><b>Spark</b><span>Ook transparante aligners op maat. Lees meer op de pagina over de <a href="{u:invisalign/}">Spark-beugel</a>.</span></li>
  <li><b>Brackets</b><span>De vaste beugel met slotjes en draden. Lees meer over <a href="{u:bracket-slotjesbeugel/}">brackets</a>.</span></li>
</ul>
<h2>Hoe werken aligners?</h2>
<p>Elke week vervangt u de aligner door een nieuwe die net iets verschilt van de vorige. Zo gaan uw tanden en kiezen stapje voor stapje naar de juiste plek. Er zijn geen metalen slotjes of draden, dus u heeft geen last van irritaties in de mond.</p>
<ul>
  <li><b>Onopvallend:</b> de aligners zijn doorzichtig en vallen vrijwel niet op.</li>
  <li><b>Makkelijk:</b> u neemt ze uit om te eten, te drinken en te poetsen.</li>
  <li><b>Flexibel:</b> bij een belangrijke afspraak kunt u ze even uitnemen.</li>
</ul>
<figure><img src="{a:assets/img/invisalign.webp}" alt="Doorzichtige aligner wordt op de tanden geplaatst" width="576" height="376" loading="lazy" decoding="async"><figcaption>Aligners zijn op maat gemaakt en nauwelijks zichtbaar.</figcaption></figure>
<div class="note"><p><b>Gratis intake orthodontie.</b> Invisalign, Spark of brackets: wat past bij u? <a href="{u:afspraak-maken/}?soort=intake-orthodontie#formulier">Vraag een gratis intake aan</a>, dan nemen wij contact met u op.</p></div>
""",
    faq=[
        ("Welke beugel past bij mij?", "Dat hangt af van uw gebit en uw wensen. Tijdens de gratis intake bekijken we uw situatie en bespreken we of aligners of brackets het meest geschikt zijn."),
        ("Hoe vaak wissel ik van aligner?", "Bij Invisalign en Spark vervangt u de aligner iedere week door een nieuwe, die net iets verschilt van de vorige."),
        ("Moet ik de aligner uitdoen als ik eet?", "Ja. U neemt de aligners uit om te eten, te drinken en te poetsen en te flossen."),
        ("Wordt een beugel vergoed?", "Beugels vallen ook voor kinderen tot 18 jaar buiten de basisverzekering. Sommige aanvullende verzekeringen vergoeden een deel, soms pas na enkele jaren verzekerd te zijn."),
    ],
    related=["esthetische-behandelingen", "preventie-en-mondhygiene", "bleken"],
)

T["vullingen"] = dict(
    title="Witte vullingen Hardenberg | Altijd composiet",
    desc="Gaatje laten vullen in Hardenberg? Bij Tandartspraktijk Badhuisplein vullen we altijd met wit composiet dat direct hard is. U kiest zelf of u verdoving wilt.",
    h1='Witte <em class="g">vullingen</em>',
    lead="Komt u voor een gaatje, dan kiest u zelf of u verdoving wilt. Vullingen maken we bij ons altijd van composiet: wit vulmateriaal dat onder een blauwe lamp direct hard wordt.",
    img="behandeling-kinan.webp", img_alt="Tandarts Kinan Khalil behandelt samen met een assistente een patiënte", img_pos="62% 40%",
    procedure="Tandvulling",
    who=["kinan", "itschi"],
    body="""
<h2>Hoe gaat het vullen van een gaatje?</h2>
<ol>
  <li><b>Verdoving, als u dat wilt.</b> Dat bepaalt u zelf.</li>
  <li><b>Schoonmaken.</b> Bij het boren komt water vrij dat de warmte beperkt en het slijpsel afvoert. De assistente zuigt dat zoveel mogelijk weg.</li>
  <li><b>Opbouwen.</b> Afhankelijk van de grootte en vorm van het gaatje gebruiken we een vormpje om de kies weer op te bouwen.</li>
  <li><b>Uitharden.</b> Een blauwe, koude lamp maakt het composiet direct hard.</li>
</ol>
<h2>Na de behandeling</h2>
<p>Van een witte vulling kunt u iets meer napijn krijgen. Dat varieert van gevoeligheid voor koud en warm tot echte kiespijn, en soms houdt het wat langer aan. Wacht bij twijfel of aanhoudende pijn niet te lang en <a href="tel:+31523216967">bel ons gerust</a>.</p>
""",
    faq=[
        ("Moet ik verdoofd worden?", "Dat kiest u zelf. Met verdoving voelt u tijdens het boren niets."),
        ("Is gevoeligheid na een vulling normaal?", "Ja, gevoeligheid voor koud en warm komt voor en gaat meestal vanzelf over. Blijft het pijnlijk, neem dan contact met ons op."),
        ("Waarom altijd composiet?", "Composiet heeft de kleur van uw tand, valt nauwelijks op en is direct hard. Daarom maken we al onze vullingen van dit materiaal."),
    ],
    related=["wortelkanaalbehandeling", "preventie-en-mondhygiene", "esthetische-behandelingen"],
)

T["extractie-trekken"] = dict(
    title="Tand of kies trekken in Hardenberg | Extractie en nazorg",
    desc="Moet er een tand of kies getrokken worden? Lees hoe een extractie bij Tandartspraktijk Badhuisplein in Hardenberg verloopt en wat u na afloop wel en niet mag.",
    h1='Een tand of kies <em class="g">trekken</em>',
    lead="Soms is een tand of kies niet meer te redden. Een extractie gebeurt onder verdoving. Hier leest u hoe u zich voorbereidt, wat er gebeurt en wat u daarna het beste kunt doen.",
    img="extractie.webp", img_alt="Tandarts Alvaro Soler en een assistente behandelen een patiënte", img_pos="62% 40%",
    procedure="Tandextractie",
    who=["kinan", "alvaro"],
    body="""
<h2>Voor de behandeling</h2>
<ul>
  <li>Eet gewoon goed voordat u komt.</li>
  <li>Vertel de tandarts of u <b>bloedverdunners</b> gebruikt, een <b>kunstmatige hartklep</b> heeft of in de afgelopen zes maanden een <b>vaatoperatie</b> heeft gehad.</li>
</ul>
<h2>De behandeling</h2>
<p>De tand of kies wordt eerst verdoofd; de verdoving moet even inwerken. Daarna wordt hij met een wrikkende, draaiende beweging verwijderd. Dat doet geen pijn, al vinden sommige mensen het een naar gevoel of geluid. Soms wordt de wond gehecht, meestal met hechtdraad die vanzelf oplost.</p>
<h2>Advies voor daarna</h2>
<ul>
  <li>Bijt <b>30 minuten</b> stevig op het steriele gaasje.</li>
  <li>U mag eten en drinken, maar <b>spoel niet</b>: de bloedprop in de holte moet blijven zitten, anders geneest de wond niet goed.</li>
  <li>Wees voorzichtig met hete drank en bijt niet op uw wang; door de verdoving voelt u minder.</li>
  <li>Doe de rest van de dag geen zwaar lichamelijk werk en drink geen alcohol.</li>
  <li>Koel uw wang zoveel mogelijk. Neem geen warm bad of hete douche en ga niet in bed liggen.</li>
  <li>Tegen pijn kunt u paracetamol of ibuprofen nemen. Ga nooit boven de maximale dosering.</li>
  <li>Probeer de eerste drie dagen niet te roken.</li>
</ul>
<div class="note"><p><b>Neem contact op</b> als het bloeden na twee uur niet is gestopt, als de koorts oploopt tot 39 °C, of als de pijn na een paar dagen toeneemt en u een vieze smaak in de mond krijgt. Dat kan wijzen op een ontsteking. Bel <a href="tel:+31523216967">0523-216967</a>; buiten openingstijden kunt u terecht bij de <a href="{u:homepage/spoedgevallen-en-weekenddienst/}">spoedpraktijk</a>.</p></div>
<h2>En daarna?</h2>
<p>Ontstaat er een zichtbare opening, dan zijn er goede oplossingen: een <a href="{u:behandelingen/implantaten/}">implantaat</a>, een <a href="{u:behandelingen/kronen-en-bruggen/}">brug</a> of een <a href="{u:behandelingen/protheses/}">prothese</a>.</p>
""",
    faq=[
        ("Doet het trekken van een kies pijn?", "Nee, de tand of kies wordt verdoofd. U kunt wel een drukkend gevoel voelen. Ook geluid of gevoel kan sommige mensen tegenvallen; zeg het gerust als u het spannend vindt."),
        ("Mag ik na het trekken eten?", "Ja, u mag gewoon eten en drinken, maar spoel niet en wees voorzichtig met hete drank zolang de verdoving werkt."),
        ("Is koorts na een extractie normaal?", "Een beetje koorts hoort bij het herstel. Loopt de koorts op tot 39 °C, neem dan contact op met de tandarts."),
    ],
    related=["implantaten", "protheses", "wortelkanaalbehandeling"],
)

T["wortelkanaalbehandeling"] = dict(
    title="Wortelkanaalbehandeling Hardenberg | Eigen tand behouden",
    desc="Ontstoken zenuw of hevige kiespijn? Met een wortelkanaalbehandeling bij Tandartspraktijk Badhuisplein in Hardenberg stoppen we de ontsteking en behoudt u uw tand.",
    h1='Wortelkanaalbehandeling: uw eigen tand <em class="g">behouden</em>',
    lead="Een ernstig ontstoken zenuw kan hevige pijn geven. Met een wortelkanaalbehandeling nemen we de oorzaak weg, zodat de ontsteking stopt en u uw tand of kies kunt behouden.",
    img="wortelkanaal.webp", img_alt="Tandarts en assistente aan het werk bij een patiënte in de stoel", img_pos="62% 40%",
    procedure="Wortelkanaalbehandeling",
    who=["itschi", "kinan"],
    body="""
<h2>Wat gebeurt er bij een wortelkanaalbehandeling?</h2>
<p>Binnen in uw tanden en kiezen zitten zenuwen en bloedvaten. Bij de wortelpunt gaan ze de wortel in en via het wortelkanaal lopen ze naar de zenuwkamer. Tijdens de behandeling worden de zenuwkamer en de wortelkanalen gereinigd en ontsmet, en daarna gevuld met een speciaal vulmateriaal.</p>
<h2>Waarom is het nodig?</h2>
<p>Een ernstig ontstoken zenuw kan hevige pijn geven en afsterven. Een afgestorven zenuw kan kaakbotverlies veroorzaken, waardoor de tand of kies los kan gaan staan en verloren kan gaan. De behandeling verhelpt de pijnklachten en voorkomt dat.</p>
<p>Een zenuw raakt ontstoken of sterft af door langdurige of kortstondig heftige irritatie, bijvoorbeeld door:</p>
<ul>
  <li>diepe cariës (gaatjes);</li>
  <li>een harde klap op de tand of kies;</li>
  <li>een barst of breuk in de tand;</li>
  <li>hevige slijtage of erosie.</li>
</ul>
<h2>Doet het pijn?</h2>
<p>Meestal kan de tand of kies goed worden verdoofd en is de behandeling niet pijnlijk. Soms is de zenuw zo ontstoken dat hij lastig te verdoven is. Ook dan kan de tandarts in de meeste gevallen pijnloos werken door extra langs de tand te verdoven. De eerste dagen na de behandeling kan de tand of kies nog licht tot flink pijnlijk zijn.</p>
<p>Bij twijfel over de ligging van wortelkanalen of een ontsteking kan een <a href="{u:cbct-rontgen/}">3D CBCT-scan</a> extra duidelijkheid geven.</p>
""",
    faq=[
        ("Doet een wortelkanaalbehandeling pijn?", "Tijdens de behandeling bent u verdoofd, dus meestal is die niet pijnlijk. De eerste dagen erna kan de tand of kies nog gevoelig of pijnlijk zijn."),
        ("Wat gebeurt er als ik niets doe?", "Een afgestorven zenuw kan kaakbotverlies veroorzaken. Daardoor kan de tand of kies los gaan staan en uiteindelijk verloren gaan."),
        ("Waardoor raakt een zenuw ontstoken?", "Onder meer door diepe gaatjes, een harde klap, een barst of breuk in de tand, of hevige slijtage."),
    ],
    related=["vullingen", "kronen-en-bruggen", "extractie-trekken"],
)

T["preventie-en-mondhygiene"] = dict(
    title="Mondhygiëne en preventie Hardenberg | Gebitsreiniging",
    desc="Bloedend tandvlees, tandsteen of een slechte adem? Het preventieteam van Tandartspraktijk Badhuisplein in Hardenberg reinigt uw gebit en geeft persoonlijk advies.",
    h1='Preventie en <em class="g">mondhygiëne</em>',
    lead="Preventie neemt bij ons een centrale plaats in. Ons team van preventie- en paro-preventieassistentes helpt u met gebitsreiniging en persoonlijk advies, zodat bloedend tandvlees tot het verleden behoort.",
    img="behandeling-anja.webp", img_alt="Preventieassistente Anja laat een patiënte het resultaat zien in een spiegel", img_pos="58% 35%",
    procedure="Gebitsreiniging en mondhygiëne",
    who=["roos", "anja", "maaike"],
    body="""
<h2>Wat doet u zelf?</h2>
<ul>
  <li>Poets twee keer per dag minstens 2 minuten, bij voorkeur met een elektrische tandenborstel.</li>
  <li>Reinig dagelijks tussen uw tanden met floss, een tandenstoker of een rager. Uw tandarts of preventieassistente adviseert welke het meest geschikt is.</li>
</ul>
<h2>Wat doet ons preventieteam?</h2>
<p>Naast een professionele reiniging krijgt u een uitgebreid, persoonlijk advies. Goede preventie betekent altijd minder gaatjes en minder behandelingen. Tijdens de periodieke controle bekijkt de tandarts of een afspraak bij de preventieassistente nodig is.</p>
<figure><img src="{a:assets/img/anja-spiegel.webp}" alt="Preventieassistente Anja bij een patiënte in de behandelstoel" width="950" height="634" loading="lazy" decoding="async"></figure>
<h2>Wanneer maakt u zelf een afspraak?</h2>
<ul>
  <li>uw tandvlees bloedt bij het poetsen;</li>
  <li>uw tandvlees is rood, gezwollen of slap, of trekt zich terug;</li>
  <li>tanden of kiezen gaan los staan;</li>
  <li>er ontstaan regelmatig gaatjes;</li>
  <li>er ontstaat vaak tandsteen en aanslag;</li>
  <li>u heeft een vieze smaak in de mond of een slechte adem.</li>
</ul>
""",
    faq=[
        ("Is bloedend tandvlees normaal?", "Nee. Bloedend tandvlees is een reden om een afspraak te maken. Met een goede reiniging en persoonlijk advies kunnen we daar vaak veel aan doen."),
        ("Hoe vaak moet ik naar de preventieassistente?", "Dat verschilt per persoon. Tijdens de periodieke controle bekijkt de tandarts of een behandeling bij de preventieassistente nodig is."),
        ("Wordt een gebitsreiniging vergoed?", "Voor kinderen tot 18 jaar valt mondzorg onder de basisverzekering. Voor volwassenen hangt het af van uw aanvullende tandartsverzekering."),
    ],
    related=["vullingen", "bleken", "esthetische-behandelingen"],
)
