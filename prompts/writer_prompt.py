writer_prompt_template = """
<START_PROMPT>
Topik: {topic}
Outline: {outline}
Konteks: {context}

Tulislah laporan akhir dalam Markdown:
- Ikuti urutan bagian pada Outline.  
- Di bawah judul, tuliskan pembuka:  
  **Update berita per [tanggal hari ini], berdasarkan hasil pencarian dalam rentang waktu [X hari/minggu/bulan/tahun terakhir].**- 
- Tulis dalam format paragraf dan bukan bullet point.
- Sertakan sumber sebagai tautan hyperlink di dalam kalimat saat data dikutip (inline).
- **Pernyataan dalam laporan harus bersumber dari klaim, jangan berhalusinasi**
- Tambahkan analisis singkat bila relevan.
- Tulis dalam Markdown
<END_PROMPT>
"""
