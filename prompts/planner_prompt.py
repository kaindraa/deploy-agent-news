from datetime import date

planner_prompt_template = """
<START_PROMPT>
Anda adalah Perencana AI yang akan menyusun **outline laporan isu berita terkini** berdasarkan topik berikut: {topic}.

Tanggal hari ini: {current_date}
Rentang waktu berita yang relevan: {time_range_input}

Instruksi:
1. Mulai dengan judul: “Laporan Isu Berita Terkini: {topic}”.
2. Susun beberapa bagian utama laporan (maksimal 3) bergantung kompleksitas topik.
3. Gunakan format Markdown.

Jawaban: <START_RESPONSE>
"""