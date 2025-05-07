writer_prompt_template = """
<START_PROMPT>
Topik: {topic}
Outline: {outline}
Konteks: {context}
Tanggal hari ini: {current_date}
Rentang waktu berita yang relevan: {time_range_input}
Tulislah laporan akhir dalam Markdown:
- Ikuti urutan bagian pada Outline.  
- Di bawah judul, tuliskan pembuka:  
  **Update berita per {current_date}, berdasarkan hasil pencarian dalam rentang waktu {time_range_input}.**- 
- Tulis dalam format paragraf dan bukan bullet point.
- Sertakan sumber sebagai tautan hyperlink di dalam kalimat saat data dikutip (inline).
- **Pernyataan dalam laporan harus bersumber dari klaim, jangan berhalusinasi**
- Tambahkan analisis singkat bila relevan.
- **Anda mungkin mendapatkan konteks yang tidak relevan, fokus pada konteks yang sesuai dengan topik dan outline**
- Tulis dalam Markdown
<END_PROMPT>
"""
