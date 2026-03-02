from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.exercise_model import Exercise

EXERCISES = [
    # SUPERIOR - Peito
    {"name": "Supino Reto", "type": "superior"},
    {"name": "Supino Inclinado", "type": "superior"},
    {"name": "Supino Declinado", "type": "superior"},
    {"name": "Supino com Halteres", "type": "superior"},
    {"name": "Supino Inclinado com Halteres", "type": "superior"},
    {"name": "Supino Vertical", "type": "superior"},
    {"name": "Supino na Máquina", "type": "superior"},
    {"name": "Supino Inclinado no Smith", "type": "superior"},
    {"name": "Crucifixo Reto", "type": "superior"},
    {"name": "Crucifixo Inclinado", "type": "superior"},
    {"name": "Crucifixo na Polia", "type": "superior"},
    {"name": "Crucifixo na Máquina", "type": "superior"},
    {"name": "Crucifixo 30° a 45° com Polia Baixa", "type": "superior"},
    {"name": "Crossover", "type": "superior"},
    {"name": "Flexão de Braço", "type": "superior"},
    {"name": "Flexão Declinada", "type": "superior"},
    {"name": "Flexão Diamante", "type": "superior"},
    {"name": "Pullover", "type": "superior"},
    {"name": "Pullover na Polia", "type": "superior"},

    # SUPERIOR - Ombros
    {"name": "Desenvolvimento com Barra", "type": "superior"},
    {"name": "Desenvolvimento com Halteres", "type": "superior"},
    {"name": "Desenvolvimento Arnold", "type": "superior"},
    {"name": "Desenvolvimento na Máquina", "type": "superior"},
    {"name": "Elevação Lateral", "type": "superior"},
    {"name": "Elevação Lateral na Polia", "type": "superior"},
    {"name": "Elevação Lateral Sentado", "type": "superior"},
    {"name": "Elevação Lateral Inclinada", "type": "superior"},
    {"name": "Elevação Frontal", "type": "superior"},
    {"name": "Elevação Frontal com Anilha", "type": "superior"},
    {"name": "Remada Alta", "type": "superior"},
    {"name": "Crucifixo Invertido", "type": "superior"},
    {"name": "Elevação Posterior com Halteres", "type": "superior"},
    {"name": "Elevação Posterior na Polia", "type": "superior"},
    {"name": "Face Pull", "type": "superior"},
    {"name": "Encolhimento com Barra", "type": "superior"},
    {"name": "Encolhimento com Halteres", "type": "superior"},
    {"name": "Encolhimento no Smith", "type": "superior"},

    # SUPERIOR - Bíceps
    {"name": "Rosca Direta com Barra", "type": "superior"},
    {"name": "Rosca Direta com Halteres", "type": "superior"},
    {"name": "Rosca Alternada", "type": "superior"},
    {"name": "Rosca Martelo", "type": "superior"},
    {"name": "Rosca Martelo na Corda", "type": "superior"},
    {"name": "Rosca Scott com Barra", "type": "superior"},
    {"name": "Rosca Scott com Halteres", "type": "superior"},
    {"name": "Rosca Scott na Máquina Supinada", "type": "superior"},
    {"name": "Rosca Concentrada", "type": "superior"},
    {"name": "Rosca 21", "type": "superior"},
    {"name": "Rosca Inversa", "type": "superior"},
    {"name": "Rosca na Polia", "type": "superior"},
    {"name": "Rosca com Barra Reta Supinada", "type": "superior"},
    {"name": "Rosca na Polia Baixa com Alças Supinada", "type": "superior"},
    {"name": "Rosca no Banco Inclinado", "type": "superior"},
    {"name": "Rosca Spider", "type": "superior"},
    {"name": "Rosca Drag", "type": "superior"},
    {"name": "Rosca Zottman", "type": "superior"},

    # SUPERIOR - Tríceps
    {"name": "Tríceps Testa", "type": "superior"},
    {"name": "Tríceps Francês", "type": "superior"},
    {"name": "Tríceps Pulley", "type": "superior"},
    {"name": "Tríceps Corda", "type": "superior"},
    {"name": "Tríceps Mergulho", "type": "superior"},
    {"name": "Tríceps Coice", "type": "superior"},
    {"name": "Supino Fechado", "type": "superior"},
    {"name": "Tríceps Unilateral", "type": "superior"},
    {"name": "Tríceps na Máquina Paralelas", "type": "superior"},
    {"name": "Tríceps Testa com Barra W Supinada", "type": "superior"},
    {"name": "Tríceps Pulley com Barra V", "type": "superior"},
    {"name": "Tríceps Pulley Unilateral", "type": "superior"},
    {"name": "Tríceps na Corda Acima da Cabeça", "type": "superior"},
    {"name": "Tríceps Banco", "type": "superior"},

    # SUPERIOR - Antebraço
    {"name": "Rosca Punho Pronada", "type": "superior"},
    {"name": "Rosca Punho Supinada", "type": "superior"},
    {"name": "Rosca Punho com Halteres", "type": "superior"},
    {"name": "Farmer Walk", "type": "superior"},

    # INFERIOR - Quadríceps
    {"name": "Agachamento Livre", "type": "inferior"},
    {"name": "Agachamento no Smith", "type": "inferior"},
    {"name": "Agachamento Frontal", "type": "inferior"},
    {"name": "Agachamento Sumô", "type": "inferior"},
    {"name": "Agachamento Búlgaro", "type": "inferior"},
    {"name": "Hack Machine", "type": "inferior"},
    {"name": "Leg Press 45°", "type": "inferior"},
    {"name": "Leg Press Horizontal", "type": "inferior"},
    {"name": "Leg Press na Máquina Articulada", "type": "inferior"},
    {"name": "Leg Press Unilateral", "type": "inferior"},
    {"name": "Cadeira Extensora", "type": "inferior"},
    {"name": "Cadeira Extensora Unilateral", "type": "inferior"},
    {"name": "Sissy Squat", "type": "inferior"},
    {"name": "Afundo", "type": "inferior"},
    {"name": "Afundo Caminhando", "type": "inferior"},
    {"name": "Afundo Inverso", "type": "inferior"},
    {"name": "Passada", "type": "inferior"},
    {"name": "Step Up", "type": "inferior"},
    {"name": "Pistol Squat", "type": "inferior"},

    # INFERIOR - Posterior
    {"name": "Levantamento Terra", "type": "posterior"},
    {"name": "Levantamento Terra Sumô", "type": "posterior"},
    {"name": "Levantamento Terra Romeno", "type": "posterior"},
    {"name": "Levantamento Terra com Trap Bar", "type": "posterior"},
    {"name": "Stiff", "type": "posterior"},
    {"name": "Stiff Unilateral", "type": "posterior"},
    {"name": "Mesa Flexora", "type": "posterior"},
    {"name": "Cadeira Flexora", "type": "posterior"},
    {"name": "Flexora em Pé", "type": "posterior"},
    {"name": "Mesa Flexora Unilateral", "type": "posterior"},
    {"name": "Nordic Curl", "type": "posterior"},
    {"name": "Good Morning", "type": "posterior"},
    {"name": "Glúteo na Máquina", "type": "posterior"},
    {"name": "Coice no Cross", "type": "posterior"},
    {"name": "Pull Through", "type": "posterior"},
    {"name": "Elevação Pélvica", "type": "posterior"},
    {"name": "Glute Bridge", "type": "posterior"},
    {"name": "Hip Thrust", "type": "posterior"},
    {"name": "Hip Thrust com Barra", "type": "posterior"},
    {"name": "Hiperextensão", "type": "posterior"},
    {"name": "Abdutor na Máquina", "type": "posterior"},
    {"name": "Adutor na Máquina", "type": "posterior"},
    {"name": "Abdutor com Caneleira", "type": "posterior"},
    {"name": "Cadeira Abdutora", "type": "posterior"},
    {"name": "Cadeira Adutora", "type": "posterior"},
    {"name": "Kettlebell Swing", "type": "posterior"},

    # INFERIOR - Panturrilha
    {"name": "Panturrilha em Pé", "type": "inferior"},
    {"name": "Panturrilha Sentado", "type": "inferior"},
    {"name": "Panturrilha no Leg Press", "type": "inferior"},
    {"name": "Panturrilha no Smith", "type": "inferior"},
    {"name": "Panturrilha Unilateral", "type": "inferior"},
    {"name": "Panturrilha no Hack", "type": "inferior"},
    {"name": "Panturrilha Donkey", "type": "inferior"},

    # POSTERIOR - Costas (Dorsal)
    {"name": "Barra Fixa", "type": "posterior"},
    {"name": "Barra Fixa Pronada", "type": "posterior"},
    {"name": "Barra Fixa Supinada", "type": "posterior"},
    {"name": "Remada Invertida", "type": "posterior"},
    {"name": "Puxada Frontal", "type": "posterior"},
    {"name": "Puxada Aberta", "type": "posterior"},
    {"name": "Puxada Triângulo", "type": "posterior"},
    {"name": "Puxada na Polia com Triângulo", "type": "posterior"},
    {"name": "Puxada Supinada", "type": "posterior"},
    {"name": "Puxada com Corda", "type": "posterior"},
    {"name": "Remada Curvada", "type": "posterior"},
    {"name": "Remada Curvada Pronada", "type": "posterior"},
    {"name": "Remada Cavalinho", "type": "posterior"},
    {"name": "Remada Unilateral com Halter", "type": "posterior"},
    {"name": "Remada Sentado", "type": "posterior"},
    {"name": "Remada Baixa", "type": "posterior"},
    {"name": "Remada Baixa Triângulo", "type": "posterior"},
    {"name": "Remada Máquina", "type": "posterior"},
    {"name": "Remada na Máquina Neutra", "type": "posterior"},
    {"name": "Remada na Máquina Articulada Supinada", "type": "posterior"},
    {"name": "Remada no Smith", "type": "posterior"},
    {"name": "Serrote", "type": "posterior"},
    {"name": "Pulldown", "type": "posterior"},
    {"name": "Remada T", "type": "posterior"},

    # CORE - Abdômen (mantive type "inferior" pra não inventar tipo novo)
    {"name": "Prancha", "type": "inferior"},
    {"name": "Prancha Lateral", "type": "inferior"},
    {"name": "Abdominal Crunch", "type": "inferior"},
    {"name": "Abdominal na Máquina", "type": "inferior"},
    {"name": "Abdominal na Polia", "type": "inferior"},
    {"name": "Elevação de Pernas", "type": "inferior"},
    {"name": "Elevação de Pernas na Barra", "type": "inferior"},
    {"name": "Russian Twist", "type": "inferior"},

    # POSTERIOR - Lombar
    {"name": "Hiperextensão Lombar", "type": "posterior"},
    {"name": "Extensão Lombar na Máquina", "type": "posterior"},
    {"name": "Superman", "type": "posterior"},
]

def seed_exercises(db: Session) -> None:
    stmt = insert(Exercise).values(EXERCISES)

    # Se já existe pelo "name", ignora aquele registro
    stmt = stmt.on_conflict_do_nothing(index_elements=["name"])

    result = db.execute(stmt)
    db.commit()

    inserted = result.rowcount or 0
    print(f"✅ Seed exercises: {inserted} novos exercícios inseridos (lista total: {len(EXERCISES)})")
