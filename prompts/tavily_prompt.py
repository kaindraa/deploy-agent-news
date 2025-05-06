tavily_planner_prompt_template = """
<START_PROMPT>
Topik: {topic}
Outline: {outline}
Konteks saat ini: {context}
Iterasi ke-{iteration_count}
Query yang sudah dicari: {searched_query}
Jumlah query baru: {max_queries}

Tugas Anda:
Buat {max_queries} query pencarian baru (boleh dalam Bahasa Indonesia atau Inggris) untuk mencari informasi yang belum tercakup di Konteks saat ini, tapi dibutuhkan oleh Outline. Hindari query yang sudah dicari.

⚠️ Aturan penting:
- Jangan gunakan ```json atau ``` di mana pun.
- Jangan gunakan newline, spasi tambahan, atau indentasi dalam output.
- Jawaban harus hanya 1 baris.
- Format jawaban: ["query 1", "query 2", ..., "query N"]
- Jangan sertakan penjelasan apa pun, hanya JSON list satu baris.
- Anda boleh menggunakan English sebagian pencarian jika terkait.

Ulangi: Jawaban Anda hanya boleh berupa **satu baris string JSON list**, tidak lebih dari {max_queries} item.

Contoh benar:
["Tren urbanisasi di Asia Tenggara", "Urbanization trend Southeast Asia", "Pengaruh urbanisasi terhadap tenaga kerja", "Impact of urban growth on labor markets"]

Jawaban:
"""
