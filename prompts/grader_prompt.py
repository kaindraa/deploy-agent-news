grader_prompt_template = """
<START_PROMPT>
Topik: {topic}
Outline: {outline}
Konteks terkumpul: {context}

Apakah hampir poin Outline sudah terisi informasi relevan dan memiliki sumber?
• Jika YA, balas: false
• Jika TIDAK, balas: true

Balasan HARUS hanya “true” atau “false” (huruf kecil).
<END_PROMPT>
"""
