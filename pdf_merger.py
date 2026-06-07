import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from PyPDF2 import PdfReader, PdfWriter


# ───────────────────────── 多語言字典 ─────────────────────────
LANG = {
    "zh": {
        "app_title":        "PDF 合併工具",
        "title_label":      "📄 PDF 合併工具",
        "btn_add":          "➕ 新增 PDF",
        "btn_edit":         "✏️ 編輯頁碼",
        "btn_up":           "⬆ 上移",
        "btn_down":         "⬇ 下移",
        "btn_delete":       "🗑 刪除",
        "btn_merge":        "🔀 合併輸出",
        "btn_lang":         "🌐 English",
        "col_no":           "#",
        "col_filename":     "檔案名稱",
        "col_total":        "總頁數",
        "col_start":        "起始頁",
        "col_end":          "結束頁",
        "col_extract":      "擷取頁數",
        "status_empty":     "尚未新增任何 PDF 檔案",
        "status_summary":   "共 {n} 個檔案，合併後總頁數：{t} 頁",
        "dlg_edit_title":   "編輯頁碼範圍",
        "dlg_edit_header":  "✏️ 設定擷取頁碼範圍",
        "lbl_file":         "檔案：",
        "lbl_total":        "總頁數：",
        "lbl_start":        "起始頁：",
        "lbl_end":          "結束頁：",
        "btn_confirm":      "✅ 確認",
        "btn_cancel":       "❌ 取消",
        "info_select":      "請先在表格中選取一個檔案",
        "hint":             "提示",
        "err_title":        "錯誤",
        "err_read":         "無法讀取檔案：\n{path}\n\n{ex}",
        "err_page_num":     "請輸入有效的頁碼數字",
        "err_page_range":   "頁碼必須在 1 ~ {n} 之間",
        "err_page_order":   "起始頁不能大於結束頁",
        "warn_title":       "警告",
        "warn_no_file":     "請先新增至少一個 PDF 檔案",
        "confirm_del":      "確認刪除",
        "confirm_del_msg":  "確定要移除「{name}」？",
        "save_dialog":      "儲存合併後的 PDF",
        "merge_done_title": "合併完成 ✅",
        "merge_done_msg":   "已成功合併 {n} 個檔案\n共 {t} 頁\n\n儲存位置：\n{path}",
        "merge_fail":       "合併失敗",
        "merge_fail_msg":   "發生錯誤：\n{ex}",
        "progress_title":   "合併中...",
        "progress_label":   "正在處理：",
        "progress_done":    "完成！",
    },
    "en": {
        "app_title":        "PDF Merger",
        "title_label":      "📄 PDF Merger",
        "btn_add":          "➕ Add PDF",
        "btn_edit":         "✏️ Edit Pages",
        "btn_up":           "⬆ Move Up",
        "btn_down":         "⬇ Move Down",
        "btn_delete":       "🗑 Delete",
        "btn_merge":        "🔀 Merge",
        "btn_lang":         "🌐 繁體中文",
        "col_no":           "#",
        "col_filename":     "Filename",
        "col_total":        "Total",
        "col_start":        "Start",
        "col_end":          "End",
        "col_extract":      "Pages",
        "status_empty":     "No PDF files added yet",
        "status_summary":   "{n} file(s) loaded, merged total: {t} page(s)",
        "dlg_edit_title":   "Edit Page Range",
        "dlg_edit_header":  "✏️ Set Page Range",
        "lbl_file":         "File:",
        "lbl_total":        "Total pages:",
        "lbl_start":        "Start page:",
        "lbl_end":          "End page:",
        "btn_confirm":      "✅ Confirm",
        "btn_cancel":       "❌ Cancel",
        "info_select":      "Please select a file in the table first",
        "hint":             "Hint",
        "err_title":        "Error",
        "err_read":         "Cannot read file:\n{path}\n\n{ex}",
        "err_page_num":     "Please enter a valid page number",
        "err_page_range":   "Page number must be between 1 and {n}",
        "err_page_order":   "Start page cannot be greater than end page",
        "warn_title":       "Warning",
        "warn_no_file":     "Please add at least one PDF file",
        "confirm_del":      "Confirm Delete",
        "confirm_del_msg":  "Remove \"{name}\"?",
        "save_dialog":      "Save Merged PDF",
        "merge_done_title": "Merge Complete ✅",
        "merge_done_msg":   "Successfully merged {n} file(s)\n{t} page(s) total\n\nSaved to:\n{path}",
        "merge_fail":       "Merge Failed",
        "merge_fail_msg":   "An error occurred:\n{ex}",
        "progress_title":   "Merging...",
        "progress_label":   "Processing:",
        "progress_done":    "Done!",
    },
}


# ───────────────────────── 資料模型 ─────────────────────────
class PDFEntry:
    def __init__(self, filepath: str, total_pages: int):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.total_pages = total_pages
        self.start_page = 1
        self.end_page = total_pages


# ───────────────────────── 主視窗 ─────────────────────────
class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_lang = "zh"          # 預設繁中
        self.pdf_entries: list[PDFEntry] = []

        self.resizable(True, True)
        self.minsize(820, 520)
        self.configure(bg="#F0F4F8")

        self._build_ui()
        self._apply_lang()                # 套用初始語言文字
        self._refresh_table()

    # ── 語言快捷取用 ─────────────────────────────────────
    def T(self, key: str, **kw) -> str:
        """取得當前語言的文字，支援 format 關鍵字。"""
        text = LANG[self.current_lang][key]
        return text.format(**kw) if kw else text

    # ── 建立 UI（只建一次，文字由 _apply_lang 填入）──────
    def _build_ui(self):
        # ── 標題列 ──
        self.title_bar = tk.Frame(self, bg="#2C3E50", pady=10)
        self.title_bar.pack(fill="x")

        self.title_label = tk.Label(
            self.title_bar,
            font=("Arial", 18, "bold"),
            bg="#2C3E50", fg="white"
        )
        self.title_label.pack(side="left", padx=20)

        # 語言切換按鈕（右上角）
        self.lang_btn = tk.Button(
            self.title_bar,
            font=("Arial", 10, "bold"),
            bg="#34495E", fg="white",
            relief="flat", padx=10, pady=4,
            cursor="hand2",
            activebackground="#4A6278", activeforeground="white",
            command=self._toggle_lang
        )
        self.lang_btn.pack(side="right", padx=16)

        # ── 主體 ──
        body = tk.Frame(self, bg="#F0F4F8", padx=16, pady=12)
        body.pack(fill="both", expand=True)

        btn_frame = tk.Frame(body, bg="#F0F4F8")
        btn_frame.pack(fill="x", pady=(0, 10))

        # 保留按鈕參考以便切換語言時更新文字
        self.btn_add    = self._btn(btn_frame, "", "#27AE60", self._add_pdf)
        self.btn_add.pack(side="left", padx=(0, 8))
        self.btn_edit   = self._btn(btn_frame, "", "#2980B9", self._edit_pages)
        self.btn_edit.pack(side="left", padx=(0, 8))
        self.btn_up     = self._btn(btn_frame, "", "#8E44AD", self._move_up)
        self.btn_up.pack(side="left", padx=(0, 8))
        self.btn_down   = self._btn(btn_frame, "", "#8E44AD", self._move_down)
        self.btn_down.pack(side="left", padx=(0, 8))
        self.btn_del    = self._btn(btn_frame, "", "#E74C3C", self._delete_entry)
        self.btn_del.pack(side="left", padx=(0, 8))
        self.btn_merge  = self._btn(btn_frame, "", "#E67E22", self._merge)
        self.btn_merge.pack(side="right")

        # ── 表格 ──
        table_frame = tk.Frame(body, bg="#F0F4F8")
        table_frame.pack(fill="both", expand=True)

        self._col_keys = ("col_no", "col_filename", "col_total",
                          "col_start", "col_end", "col_extract")
        columns = tuple(range(len(self._col_keys)))   # 暫用數字，_apply_lang 再填文字
        self.tree = ttk.Treeview(table_frame, columns=self._col_keys,
                                 show="headings", height=14)

        col_widths = [40, 360, 80, 80, 80, 80]
        for key, w in zip(self._col_keys, col_widths):
            self.tree.column(key, width=w,
                             anchor="w" if key == "col_filename" else "center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", lambda e: self._edit_pages())

        # ── 狀態列 ──
        self.status_var = tk.StringVar()
        status_bar = tk.Frame(self, bg="#BDC3C7", pady=4)
        status_bar.pack(fill="x", side="bottom")
        tk.Label(
            status_bar, textvariable=self.status_var,
            bg="#BDC3C7", fg="#2C3E50", font=("Arial", 10)
        ).pack(side="left", padx=10)

        # ── 樣式 ──
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=28, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"),
                        background="#2C3E50", foreground="white")
        style.map("Treeview", background=[("selected", "#2980B9")])

    # ── 套用語言（更新所有文字）────────────────────────────
    def _apply_lang(self):
        self.title(self.T("app_title"))
        self.title_label.config(text=self.T("title_label"))
        self.lang_btn.config(text=self.T("btn_lang"))

        self.btn_add.config(text=self.T("btn_add"))
        self.btn_edit.config(text=self.T("btn_edit"))
        self.btn_up.config(text=self.T("btn_up"))
        self.btn_down.config(text=self.T("btn_down"))
        self.btn_del.config(text=self.T("btn_delete"))
        self.btn_merge.config(text=self.T("btn_merge"))

        for key in self._col_keys:
            self.tree.heading(key, text=self.T(key))

        self._refresh_table()   # 狀態列文字也一起刷新

    # ── 切換語言 ─────────────────────────────────────────
    def _toggle_lang(self):
        self.current_lang = "en" if self.current_lang == "zh" else "zh"
        self._apply_lang()

    @staticmethod
    def _btn(parent, text, color, cmd):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", padx=12, pady=6,
            cursor="hand2",
            activebackground=color, activeforeground="white"
        )

    # ── 刷新表格 ─────────────────────────────────────────
    def _refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        total = 0
        for i, e in enumerate(self.pdf_entries, 1):
            pages = e.end_page - e.start_page + 1
            total += pages
            self.tree.insert("", "end", iid=str(i - 1), values=(
                i, e.filename, e.total_pages,
                e.start_page, e.end_page, pages
            ))
        if self.pdf_entries:
            self.status_var.set(self.T("status_summary",
                                       n=len(self.pdf_entries), t=total))
        else:
            self.status_var.set(self.T("status_empty"))

    def _selected_index(self) -> int | None:
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    # ── 新增 PDF ─────────────────────────────────────────
    def _add_pdf(self):
        paths = filedialog.askopenfilenames(
            title=self.T("btn_add"),
            filetypes=[("PDF", "*.pdf")]
        )
        for path in paths:
            try:
                reader = PdfReader(path)
                total = len(reader.pages)
                self.pdf_entries.append(PDFEntry(path, total))
            except Exception as ex:
                messagebox.showerror(
                    self.T("err_title"),
                    self.T("err_read", path=path, ex=ex)
                )
        self._refresh_table()

    def _edit_pages(self):
        idx = self._selected_index()
        if idx is None:
            messagebox.showinfo(self.T("hint"), self.T("info_select"))
            return
        PageEditDialog(self, self.pdf_entries[idx], self._refresh_table)

    def _move_up(self):
        idx = self._selected_index()
        if idx is None or idx == 0:
            return
        self.pdf_entries[idx - 1], self.pdf_entries[idx] = \
            self.pdf_entries[idx], self.pdf_entries[idx - 1]
        self._refresh_table()
        self.tree.selection_set(str(idx - 1))

    def _move_down(self):
        idx = self._selected_index()
        if idx is None or idx >= len(self.pdf_entries) - 1:
            return
        self.pdf_entries[idx], self.pdf_entries[idx + 1] = \
            self.pdf_entries[idx + 1], self.pdf_entries[idx]
        self._refresh_table()
        self.tree.selection_set(str(idx + 1))

    def _delete_entry(self):
        idx = self._selected_index()
        if idx is None:
            messagebox.showinfo(self.T("hint"), self.T("info_select"))
            return
        name = self.pdf_entries[idx].filename
        if messagebox.askyesno(self.T("confirm_del"),
                               self.T("confirm_del_msg", name=name)):
            self.pdf_entries.pop(idx)
            self._refresh_table()

    # ── 合併（帶進度條）──────────────────────────────────
    def _merge(self):
        if not self.pdf_entries:
            messagebox.showwarning(self.T("warn_title"), self.T("warn_no_file"))
            return

        save_path = filedialog.asksaveasfilename(
            title=self.T("save_dialog"),
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")]
        )
        if not save_path:
            return

        # 計算總頁數（進度條最大值）
        total_pages = sum(e.end_page - e.start_page + 1 for e in self.pdf_entries)

        # 開啟進度視窗
        prog_dlg = MergeProgressDialog(self, total_pages)

        # 在背景執行緒執行合併，避免 UI 凍結
        def worker():
            try:
                writer = PdfWriter()
                done = 0
                for entry in self.pdf_entries:
                    # 更新當前處理的檔名
                    self.after(0, prog_dlg.set_filename, entry.filename)
                    reader = PdfReader(entry.filepath)
                    for page_num in range(entry.start_page - 1, entry.end_page):
                        writer.add_page(reader.pages[page_num])
                        done += 1
                        self.after(0, prog_dlg.set_progress, done)

                with open(save_path, "wb") as f:
                    writer.write(f)

                # 完成：關閉進度視窗，顯示成功訊息
                self.after(0, prog_dlg.finish)
                self.after(0, messagebox.showinfo,
                           self.T("merge_done_title"),
                           self.T("merge_done_msg",
                                  n=len(self.pdf_entries),
                                  t=total_pages,
                                  path=save_path))
            except Exception as ex:
                self.after(0, prog_dlg.finish)
                self.after(0, messagebox.showerror,
                           self.T("merge_fail"),
                           self.T("merge_fail_msg", ex=ex))

        threading.Thread(target=worker, daemon=True).start()


# ───────────────────────── 合併進度條對話框 ─────────────────────────
class MergeProgressDialog(tk.Toplevel):
    def __init__(self, parent: PDFMergerApp, total_pages: int):
        super().__init__(parent)
        self._parent = parent
        self._total = total_pages

        self.title(parent.T("progress_title"))
        self.resizable(False, False)
        self.configure(bg="#F0F4F8", padx=30, pady=24)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: None)   # 禁止手動關閉

        self._build_ui()
        self._center()

    def _build_ui(self):
        tk.Label(
            self, text="🔀 " + self._parent.T("progress_title"),
            font=("Arial", 13, "bold"), bg="#F0F4F8", fg="#2C3E50"
        ).pack(pady=(0, 12))

        # 當前處理檔名
        self._file_var = tk.StringVar(value="")
        self._prefix_label = self._parent.T("progress_label")
        self._file_label = tk.Label(
            self, textvariable=self._file_var,
            font=("Arial", 10), bg="#F0F4F8", fg="#555555",
            wraplength=340, justify="left"
        )
        self._file_label.pack(anchor="w", pady=(0, 8))

        # 進度條
        self._prog_var = tk.IntVar(value=0)
        self._bar = ttk.Progressbar(
            self, orient="horizontal", length=360,
            mode="determinate", maximum=self._total,
            variable=self._prog_var
        )
        self._bar.pack(pady=(0, 8))

        # 百分比文字
        self._pct_var = tk.StringVar(value="0 %")
        tk.Label(
            self, textvariable=self._pct_var,
            font=("Arial", 11, "bold"), bg="#F0F4F8", fg="#2980B9"
        ).pack()

    def set_filename(self, name: str):
        self._file_var.set(f"{self._prefix_label}  {name}")

    def set_progress(self, done: int):
        self._prog_var.set(done)
        pct = int(done / self._total * 100) if self._total else 100
        self._pct_var.set(f"{pct} %")
        self.update_idletasks()

    def finish(self):
        self._pct_var.set(self._parent.T("progress_done"))
        self.after(400, self.destroy)   # 短暫停留後關閉

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = self.master.winfo_rootx() + (self.master.winfo_width()  - w) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - h) // 2
        self.geometry(f"+{x}+{y}")


# ───────────────────────── 頁碼編輯對話框 ─────────────────────────
class PageEditDialog(tk.Toplevel):
    def __init__(self, parent: PDFMergerApp, entry: PDFEntry, on_save_callback):
        super().__init__(parent)
        self._parent = parent
        self.entry = entry
        self.on_save_callback = on_save_callback

        self.title(parent.T("dlg_edit_title"))
        self.resizable(False, False)
        self.configure(bg="#F0F4F8", padx=30, pady=24)
        self.grab_set()

        self._build_ui()
        self._center()

    def _build_ui(self):
        p = self._parent   # 語言快捷

        tk.Label(
            self, text=p.T("dlg_edit_header"),
            font=("Arial", 14, "bold"), bg="#F0F4F8", fg="#2C3E50"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 16))

        tk.Label(self, text=p.T("lbl_file"),
                 font=("Arial", 11), bg="#F0F4F8").grid(row=1, column=0, sticky="e", pady=4)
        tk.Label(
            self, text=self.entry.filename,
            font=("Arial", 11, "bold"), bg="#F0F4F8", fg="#2980B9",
            wraplength=280, justify="left"
        ).grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(self, text=p.T("lbl_total"),
                 font=("Arial", 11), bg="#F0F4F8").grid(row=2, column=0, sticky="e", pady=4)
        tk.Label(
            self, text=str(self.entry.total_pages),
            font=("Arial", 11), bg="#F0F4F8", fg="#27AE60"
        ).grid(row=2, column=1, sticky="w", pady=4)

        tk.Label(self, text=p.T("lbl_start"),
                 font=("Arial", 11), bg="#F0F4F8").grid(row=3, column=0, sticky="e", pady=6)
        self.start_var = tk.IntVar(value=self.entry.start_page)
        tk.Spinbox(
            self, from_=1, to=self.entry.total_pages,
            textvariable=self.start_var,
            font=("Arial", 12), width=8, justify="center"
        ).grid(row=3, column=1, sticky="w", pady=6)

        tk.Label(self, text=p.T("lbl_end"),
                 font=("Arial", 11), bg="#F0F4F8").grid(row=4, column=0, sticky="e", pady=6)
        self.end_var = tk.IntVar(value=self.entry.end_page)
        tk.Spinbox(
            self, from_=1, to=self.entry.total_pages,
            textvariable=self.end_var,
            font=("Arial", 12), width=8, justify="center"
        ).grid(row=4, column=1, sticky="w", pady=6)

        ttk.Separator(self, orient="horizontal").grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=14
        )

        btn_frame = tk.Frame(self, bg="#F0F4F8")
        btn_frame.grid(row=6, column=0, columnspan=2)

        tk.Button(
            btn_frame, text=p.T("btn_confirm"), command=self._save,
            bg="#27AE60", fg="white", font=("Arial", 11, "bold"),
            relief="flat", padx=16, pady=6, cursor="hand2",
            activebackground="#27AE60", activeforeground="white"
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            btn_frame, text=p.T("btn_cancel"), command=self.destroy,
            bg="#E74C3C", fg="white", font=("Arial", 11, "bold"),
            relief="flat", padx=16, pady=6, cursor="hand2",
            activebackground="#E74C3C", activeforeground="white"
        ).pack(side="left")

    def _save(self):
        p = self._parent
        try:
            start = self.start_var.get()
            end   = self.end_var.get()
        except tk.TclError:
            messagebox.showerror(p.T("err_title"), p.T("err_page_num"), parent=self)
            return

        if start < 1 or end > self.entry.total_pages:
            messagebox.showerror(
                p.T("err_title"),
                p.T("err_page_range", n=self.entry.total_pages),
                parent=self
            )
            return
        if start > end:
            messagebox.showerror(p.T("err_title"), p.T("err_page_order"), parent=self)
            return

        self.entry.start_page = start
        self.entry.end_page   = end
        self.on_save_callback()
        self.destroy()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = self.master.winfo_rootx() + (self.master.winfo_width()  - w) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - h) // 2
        self.geometry(f"+{x}+{y}")


# ───────────────────────── 程式入口 ─────────────────────────
if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()