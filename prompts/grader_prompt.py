grader_prompt_template = """
<START_PROMPT>
Topik: {topic}
Outline: {outline}
Konteks terkumpul: {context}

Apakah poin Outline sudah terisi informasi relevan dan memiliki sumber **bersikap kritis, apakah memang sudah relevan dan bersumber**?
• Jika YA, balas: false
• Jika TIDAK, balas: true

Balasan HARUS hanya “true” atau “false” (huruf kecil).
<END_PROMPT>
"""
