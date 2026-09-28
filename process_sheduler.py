
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

#Punteros

class Node:
    def __init__(self, process_id: str, name: str, priority: int):
        self.process_id = process_id
        self.name = name
        self.priority = priority
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.prev = None          # puntero previo
        self.next = None          # Puntero que pasa al siguiente


class DoublyLinkedList:

    def __init__(self):
        self.head = None          # cabeza
        self.tail = None          # cola
        self.current = None       # proceso
        self.size = 0

    def is_empty(self) -> bool:
        return self.head is None

    def append(self, process_id: str, name: str, priority: int) -> str:
        """Add a new process at the end (most recent)"""
        new_node = Node(process_id, name, priority)

        if self.is_empty():
            self.head = self.tail = self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.current = new_node          # proceso actual

        self.size += 1
        return f"Process {process_id} ({name}) added to history"

    def prepend(self, process_id: str, name: str, priority: int) -> str:
        """Add a process at the beginning (oldest position)"""
        new_node = Node(process_id, name, priority)

        if self.is_empty():
            self.head = self.tail = self.current = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1
        return f"Process {process_id} inserted at the beginning"

    def remove_by_id(self, process_id: str) -> str:
        """Remove a process by its ID using pointers"""
        if self.is_empty():
            return "History is empty"

        node = self.head
        while node:
            if node.process_id == process_id:
                if node.prev:
                    node.prev.next = node.next
                else:
                    self.head = node.next          # detener cabeza

                if node.next:
                    node.next.prev = node.prev
                else:
                    self.tail = node.prev          # detener cola

                # arreglar punteros
                if self.current == node:
                    self.current = node.next if node.next else node.prev

                self.size -= 1
                return f"Process {process_id} killed and removed from history"

            node = node.next

        return f"Process {process_id} not found"

    def move_forward(self) -> str:
        """Move current pointer to the next process (newer)"""
        if not self.current:
            return "No process selected"
        if self.current.next is None:
            return "Already at the most recent process"
        self.current = self.current.next
        return f"Moved forward → {self.current.process_id} ({self.current.name})"

    def move_backward(self) -> str:
        """Move current pointer to the previous process (older)"""
        if not self.current:
            return "No process selected"
        if self.current.prev is None:
            return "Already at the oldest process"
        self.current = self.current.prev
        return f"Moved backward → {self.current.process_id} ({self.current.name})"

    def go_to_head(self) -> str:
        """Jump to the oldest process"""
        if self.is_empty():
            return "History is empty"
        self.current = self.head
        return f"Jumped to oldest → {self.current.process_id}"

    def go_to_tail(self) -> str:
        """Jump to the most recent process"""
        if self.is_empty():
            return "History is empty"
        self.current = self.tail
        return f"Jumped to newest → {self.current.process_id}"

    def get_current(self) -> str:
        if not self.current:
            return "No process selected"
        return (f"ID: {self.current.process_id} | Name: {self.current.name} | "
                f"Priority: {self.current.priority} | Time: {self.current.timestamp}")

    def get_all_forward(self) -> list:
        """Traverse from head to tail using next pointers"""
        result = []
        node = self.head
        while node:
            marker = " ◀ CURRENT" if node == self.current else ""
            result.append(f"{node.process_id} | {node.name} | P{node.priority} | {node.timestamp}{marker}")
            node = node.next
        return result

    def get_all_backward(self) -> list:
        """Traverse from tail to head using prev pointers"""
        result = []
        node = self.tail
        while node:
            marker = " ◀ CURRENT" if node == self.current else ""
            result.append(f"{node.process_id} | {node.name} | P{node.priority} | {node.timestamp}{marker}")
            node = node.prev
        return result


#desplegar frontend en tkinter

class ProcessSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process History Scheduler - Doubly Linked List")
        self.root.geometry("950x650")
        self.root.configure(bg="#1e1e2e")

        self.history = DoublyLinkedList()
        self.process_counter = 1000

        self._build_ui()
        self._load_sample_data()
        self._refresh()

    def _build_ui(self):
        # Title
        tk.Label(self.root, text="Process History Scheduler",
                 font=("Segoe UI", 18, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=10)
        tk.Label(self.root, text="Doubly Linked List (prev + next pointers)",
                 font=("Segoe UI", 10), bg="#1e1e2e", fg="#a6adc8").pack()

        main = tk.Frame(self.root, bg="#1e1e2e")
        main.pack(fill="both", expand=True, padx=15, pady=10)

        # ----- Left panel: Controls -----
        left = tk.Frame(main, bg="#313244", padx=15, pady=15)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Add New Process", font=("Segoe UI", 12, "bold"),
                 bg="#313244", fg="#cdd6f4").pack(anchor="w")

        tk.Label(left, text="Process Name:", bg="#313244", fg="#cdd6f4").pack(anchor="w", pady=(8, 0))
        self.entry_name = tk.Entry(left, width=22, font=("Segoe UI", 11))
        self.entry_name.pack(pady=3)

        tk.Label(left, text="Priority (1-10):", bg="#313244", fg="#cdd6f4").pack(anchor="w")
        self.entry_priority = tk.Entry(left, width=22, font=("Segoe UI", 11))
        self.entry_priority.insert(0, "5")
        self.entry_priority.pack(pady=3)

        tk.Button(left, text="Add Process (Append)", bg="#a6e3a1", fg="#1e1e2e",
                  font=("Segoe UI", 10, "bold"), command=self._add_process).pack(pady=8, fill="x")

        tk.Button(left, text="Insert at Beginning", bg="#89b4fa", fg="#1e1e2e",
                  command=self._prepend_process).pack(pady=4, fill="x")

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=12)

        tk.Label(left, text="Navigation (Pointers)", font=("Segoe UI", 12, "bold"),
                 bg="#313244", fg="#cdd6f4").pack(anchor="w")

        nav = tk.Frame(left, bg="#313244")
        nav.pack(pady=6)
        tk.Button(nav, text="◀ Backward", width=10, bg="#f9e2af", fg="#1e1e2e",
                  command=self._move_backward).pack(side="left", padx=3)
        tk.Button(nav, text="Forward ▶", width=10, bg="#f9e2af", fg="#1e1e2e",
                  command=self._move_forward).pack(side="left", padx=3)

        tk.Button(left, text="Go to Oldest (Head)", bg="#fab387", fg="#1e1e2e",
                  command=self._go_head).pack(pady=4, fill="x")
        tk.Button(left, text="Go to Newest (Tail)", bg="#fab387", fg="#1e1e2e",
                  command=self._go_tail).pack(pady=4, fill="x")

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=12)

        tk.Label(left, text="Kill Process (by ID):", bg="#313244", fg="#cdd6f4").pack(anchor="w")
        self.entry_kill = tk.Entry(left, width=22, font=("Segoe UI", 11))
        self.entry_kill.pack(pady=3)
        tk.Button(left, text="Kill Process", bg="#f38ba8", fg="#1e1e2e",
                  font=("Segoe UI", 10, "bold"), command=self._kill_process).pack(pady=6, fill="x")

        # ----- Right panel: Views -----
        right = tk.Frame(main, bg="#1e1e2e")
        right.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Current process
        tk.Label(right, text="Current Process (pointer)", font=("Segoe UI", 11, "bold"),
                 bg="#1e1e2e", fg="#94e2d5").pack(anchor="w")
        self.lbl_current = tk.Label(right, text="—", font=("Consolas", 11),
                                    bg="#313244", fg="#cdd6f4", anchor="w", padx=10, pady=8)
        self.lbl_current.pack(fill="x", pady=4)

        # History forward
        tk.Label(right, text="History (Head → Tail)  using next pointers",
                 font=("Segoe UI", 11, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(anchor="w", pady=(10, 0))
        self.txt_forward = scrolledtext.ScrolledText(right, height=8, font=("Consolas", 10),
                                                     bg="#313244", fg="#cdd6f4")
        self.txt_forward.pack(fill="x", pady=4)

        # History backward
        tk.Label(right, text="History (Tail → Head)  using prev pointers",
                 font=("Segoe UI", 11, "bold"), bg="#1e1e2e", fg="#cba6f7").pack(anchor="w", pady=(8, 0))
        self.txt_backward = scrolledtext.ScrolledText(right, height=6, font=("Consolas", 10),
                                                      bg="#313244", fg="#cdd6f4")
        self.txt_backward.pack(fill="x", pady=4)

        # Log
        tk.Label(right, text="System Log", font=("Segoe UI", 11, "bold"),
                 bg="#1e1e2e", fg="#a6e3a1").pack(anchor="w", pady=(8, 0))
        self.txt_log = scrolledtext.ScrolledText(right, height=6, font=("Consolas", 10),
                                                 bg="#11111b", fg="#a6e3a1")
        self.txt_log.pack(fill="both", expand=True, pady=4)

    def _log(self, msg: str):
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)

    def _refresh(self):
        # Current
        self.lbl_current.config(text=self.history.get_current())

        # Forward traversal
        self.txt_forward.delete("1.0", tk.END)
        items = self.history.get_all_forward()
        self.txt_forward.insert(tk.END, "\n".join(items) if items else "(empty)")

        # Backward traversal
        self.txt_backward.delete("1.0", tk.END)
        items = self.history.get_all_backward()
        self.txt_backward.insert(tk.END, "\n".join(items) if items else "(empty)")

    def _add_process(self):
        name = self.entry_name.get().strip() or "Unknown"
        try:
            priority = int(self.entry_priority.get())
        except ValueError:
            priority = 5
        self.process_counter += 1
        pid = f"P{self.process_counter}"
        msg = self.history.append(pid, name, priority)
        self._log(msg)
        self.entry_name.delete(0, tk.END)
        self._refresh()

    def _prepend_process(self):
        name = self.entry_name.get().strip() or "Unknown"
        try:
            priority = int(self.entry_priority.get())
        except ValueError:
            priority = 5
        self.process_counter += 1
        pid = f"P{self.process_counter}"
        msg = self.history.prepend(pid, name, priority)
        self._log(msg)
        self._refresh()

    def _move_forward(self):
        msg = self.history.move_forward()
        self._log(msg)
        self._refresh()

    def _move_backward(self):
        msg = self.history.move_backward()
        self._log(msg)
        self._refresh()

    def _go_head(self):
        msg = self.history.go_to_head()
        self._log(msg)
        self._refresh()

    def _go_tail(self):
        msg = self.history.go_to_tail()
        self._log(msg)
        self._refresh()

    def _kill_process(self):
        pid = self.entry_kill.get().strip().upper()
        if not pid:
            messagebox.showwarning("Warning", "Enter a Process ID")
            return
        msg = self.history.remove_by_id(pid)
        self._log(msg)
        self.entry_kill.delete(0, tk.END)
        self._refresh()

    def _load_sample_data(self):
        samples = [
            ("P1001", "System Init", 1),
            ("P1002", "Network Service", 3),
            ("P1003", "User Login", 5),
            ("P1004", "File Explorer", 4),
            ("P1005", "Browser", 6),
        ]
        for pid, name, prio in samples:
            self.history.append(pid, name, prio)
        self.process_counter = 1005
        self._log("Sample process history loaded.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessSchedulerApp(root)
    root.mainloop()