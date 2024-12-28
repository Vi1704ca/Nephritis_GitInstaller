import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil


directory = os.path.dirname(__file__)


LINK_ICON = os.path.join(os.path.dirname(__file__), "assets", "icon_Ebp_icon.ico")
PRIMARY_COLOR = "#104d02"  
SECONDARY_COLOR = "#104d02"  
BACKGROUND_COLOR = "#337418"  
HOVER_COLOR_S = "#0C3C01"
FONT_COLOR = "#FFFFFF"  


app = ctk.CTk()

class GitHubHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nephritis")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.iconbitmap(LINK_ICON)

        self.MY_FONT_Title = ctk.CTkFont(family="Times New Roman", size=28, weight="bold")
        self.MY_FONT_Paragraph = ctk.CTkFont(family="Times New Roman", size=18, weight="bold")

        self.current_page = None

        self.clone_page = ctk.CTkFrame(self.root, fg_color=BACKGROUND_COLOR)
        self.upload_page = ctk.CTkFrame(self.root, fg_color=BACKGROUND_COLOR)

        self.create_clone_page()
        self.create_upload_page()

        self.show_page(self.clone_page)

    def create_clone_page(self):
        ctk.CTkLabel(self.clone_page, text="Cloning a repository", text_color=FONT_COLOR, font=self.MY_FONT_Title).pack(pady=25)

        ctk.CTkLabel(self.clone_page, text="Repository link:", text_color=FONT_COLOR, font=self.MY_FONT_Paragraph).pack(pady=10)
        self.clone_repo_url = ctk.CTkEntry(self.clone_page, width=450, height=30, border_color="#1C342C", border_width=6, fg_color="#0F0F0F", corner_radius=15, text_color="#c2c1c0", font=self.MY_FONT_Paragraph)
        self.clone_repo_url.pack(pady=(10, 25))

        ctk.CTkLabel(self.clone_page, text="Installation path:", text_color=FONT_COLOR, font=self.MY_FONT_Paragraph).pack(pady=5)
        self.clone_path = ctk.CTkEntry(self.clone_page, width=450, height=30, border_color="#1C342C", border_width=6, fg_color="#0F0F0F", corner_radius=15, text_color="#c2c1c0", font=self.MY_FONT_Paragraph)
        self.clone_path.pack(pady=(15,20))

        ctk.CTkButton(self.clone_page, text="Select folder", command=self.select_folder, fg_color=PRIMARY_COLOR, text_color=FONT_COLOR, font=self.MY_FONT_Paragraph, hover_color=HOVER_COLOR_S).pack(pady=(60, 40))
        ctk.CTkButton(self.clone_page, text="Clone", command=self.clone_repo, fg_color=SECONDARY_COLOR, text_color=FONT_COLOR, font=self.MY_FONT_Paragraph, hover_color=HOVER_COLOR_S).pack(pady=15)

        ctk.CTkButton(self.clone_page, text="\u2192", command=lambda: self.show_page(self.upload_page), fg_color=PRIMARY_COLOR, text_color=FONT_COLOR, width=50, hover_color=HOVER_COLOR_S, font=self.MY_FONT_Paragraph).pack(side="bottom", pady=10)

    def create_upload_page(self):
        ctk.CTkLabel(self.upload_page, text="Uploading a file to the repository", text_color=FONT_COLOR, font=self.MY_FONT_Title).pack(pady=25)

        ctk.CTkLabel(self.upload_page, text="Repository link:", text_color=FONT_COLOR, font=self.MY_FONT_Paragraph).pack(pady=(5, 10))
        self.upload_repo_url = ctk.CTkEntry(self.upload_page, width=450, height=30, border_color="#1C342C", border_width=6, fg_color="#0F0F0F", corner_radius=15, text_color="#c2c1c0", font=self.MY_FONT_Paragraph)
        self.upload_repo_url.pack(pady=(10, 5))

        ctk.CTkLabel(self.upload_page, text="Path to file to download:", text_color=FONT_COLOR, font=self.MY_FONT_Paragraph).pack(pady=(10, 5))

        frame_file = ctk.CTkFrame(self.upload_page, fg_color=BACKGROUND_COLOR)
        frame_file.pack(pady=(10, 10))

        self.upload_file_path = ctk.CTkEntry(frame_file, width=410, height=30, border_color="#1C342C", border_width=6, fg_color="#0F0F0F", corner_radius=15, text_color="#c2c1c0", font=self.MY_FONT_Paragraph, bg_color=BACKGROUND_COLOR)
        self.upload_file_path.pack(side="left", padx=(0, 10))

        ctk.CTkButton(frame_file, text="Select file", command=self.select_file, fg_color=PRIMARY_COLOR, text_color=FONT_COLOR, bg_color=BACKGROUND_COLOR, font=self.MY_FONT_Paragraph, hover_color=HOVER_COLOR_S).pack(padx=(0, 10))
        
        ctk.CTkLabel(self.upload_page, text="Commit comment:", text_color=FONT_COLOR, font=self.MY_FONT_Paragraph).pack(pady=(8, 10))
        self.commit_message = ctk.CTkEntry(self.upload_page, width=350, height=30, border_color="#1C342C", border_width=6, fg_color="#0F0F0F", corner_radius=15, text_color="#c2c1c0", font=self.MY_FONT_Paragraph)
        self.commit_message.pack(pady=5)

        ctk.CTkLabel(self.upload_page, text="Branch name:", text_color=FONT_COLOR, font=self.MY_FONT_Paragraph).pack(pady=(8, 10))
        self.branch_name = ctk.CTkEntry(self.upload_page, width=150, height=30, border_color="#1C342C", border_width=6, fg_color="#0F0F0F", corner_radius=15, text_color="#c2c1c0", font=self.MY_FONT_Paragraph)
        self.branch_name.pack(pady=(5, 10))

        ctk.CTkButton(self.upload_page, text="Download", command=self.upload_file, fg_color=SECONDARY_COLOR, text_color=FONT_COLOR, font=self.MY_FONT_Paragraph, hover_color=HOVER_COLOR_S).pack(pady=(25, 5))

        ctk.CTkButton(self.upload_page, text="\u2190", command=lambda: self.show_page(self.clone_page), fg_color=PRIMARY_COLOR, text_color=FONT_COLOR, width=50, font=self.MY_FONT_Paragraph, hover_color=HOVER_COLOR_S).pack(side="bottom", pady=10)

    def show_page(self, page):
        if self.current_page:
            self.current_page.pack_forget()
        page.pack(fill="both", expand=True)
        self.current_page = page

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select a folder to clone")
        if folder:
            self.clone_path.delete(0, ctk.END)
            self.clone_path.insert(0, folder)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select file to upload")
        if file_path:
            self.upload_file_path.delete(0, ctk.END)
            self.upload_file_path.insert(0, file_path)

    def clone_repo(self):
        repo_url = self.clone_repo_url.get()
        repo_name = os.path.basename(repo_url.rstrip('/')).replace('.git', '')
        install_path = self.clone_path.get()

        if not repo_url.strip() or not install_path.strip():
            messagebox.showwarning("Error", "Please provide a link to the repository and the path to clone.")
            return

        try:
            unique_folder = os.path.join(install_path, repo_name)
            os.makedirs(unique_folder, exist_ok=True)

            subprocess.run(["git", "clone", repo_url, unique_folder], check=True)
            messagebox.showinfo("Success", f"The repository has been successfully cloned to {unique_folder}")
            self.repo_path = unique_folder  
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Error cloning repository.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def upload_file(self):
        repo_url = self.upload_repo_url.get()
        file_path = self.upload_file_path.get()
        commit_message = self.commit_message.get()
        branch_name = self.branch_name.get()

        if not repo_url.strip() or not file_path.strip() or not commit_message.strip() or not branch_name.strip():
            messagebox.showwarning("Error", "All fields must be filled in.")
            return

        try:
            # Создаём временную директорию, если репозиторий ещё не клонирован
            if not hasattr(self, 'repo_path'):
                self.repo_path = os.path.join(os.getcwd(), f"temp_repo_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

            # Если репозиторий ещё не клонирован, клонируем его
            if not os.path.exists(self.repo_path):
                subprocess.run(["git", "clone", repo_url, self.repo_path], check=True)

            # Переходим в директорию репозитория
            os.chdir(self.repo_path)

            # Проверяем, существует ли ветка
            branches = subprocess.run(["git", "branch", "--list", branch_name], capture_output=True, text=True)
            if branch_name not in branches.stdout:
                subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            else:
                subprocess.run(["git", "checkout", branch_name], check=True)

            # Получаем изменения с удалённого репозитория
            subprocess.run(["git", "pull", "origin", branch_name], check=False)

            # Копируем файл в репозиторий
            shutil.copy(file_path, self.repo_path)

            # Добавляем и коммитим изменения
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)

            # Отправляем изменения на удалённый репозиторий
            subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

            messagebox.showinfo("Success", f"The file has been successfully uploaded to the repository on the branch {branch_name}.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error while executing git command: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



if __name__ == "__main__":
    app = ctk.CTk()
    GitHubHelperApp(app)
    app.mainloop()
