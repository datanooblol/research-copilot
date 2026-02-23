import curses
import tempfile
import subprocess
import os
from storage import Storage
from paper import Paper

class ResearchApp:
    def __init__(self):
        self.storage = Storage()
        self.selected_paper = 0
        self.mode = "view"  # view, add_paper, edit_section, edit_metadata
    
    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Draw split panes
            self.draw_left_pane(stdscr, height, width)
            self.draw_right_pane(stdscr, height, width)
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('a') or key == ord('A'):
                self.add_paper_flow(stdscr)
            elif key == ord('d') or key == ord('D'):
                self.delete_paper()
            elif key == ord('e') or key == ord('E'):
                self.edit_metadata_flow(stdscr)
            elif key == ord('1'):
                self.view_section(stdscr, "objective")
            elif key == ord('2'):
                self.view_section(stdscr, "methodology")
            elif key == ord('3'):
                self.view_section(stdscr, "conclusion")
            elif key == curses.KEY_UP:
                self.selected_paper = max(0, self.selected_paper - 1)
            elif key == curses.KEY_DOWN:
                self.selected_paper = min(len(self.storage.papers) - 1, self.selected_paper + 1)
    
    def draw_left_pane(self, stdscr, height, width):
        left_width = width // 3
        
        # Header
        stdscr.addstr(0, 0, "═" * left_width)
        title = f" PAPERS ({len(self.storage.papers)}) "
        stdscr.addstr(0, 2, title)
        stdscr.addstr(1, 0, "═" * left_width)
        
        # Papers list
        papers = self.storage.get_papers()
        if not papers:
            stdscr.addstr(3, 2, "No papers yet")
        else:
            for i, paper in enumerate(papers):
                y = 3 + i
                if y >= height - 3:
                    break
                
                # Indicators
                indicators = ""
                indicators += "✓" if paper.is_section_filled("objective") else "○"
                indicators += "✓" if paper.is_section_filled("methodology") else "○"
                indicators += "✓" if paper.is_section_filled("conclusion") else "○"
                
                line = f" {paper.get_short_title()} {indicators}"
                if i == self.selected_paper:
                    stdscr.addstr(y, 0, "►" + line[:left_width-2], curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 0, " " + line[:left_width-2])
        
        # Footer
        stdscr.addstr(height - 2, 0, "─" * left_width)
        stdscr.addstr(height - 1, 0, "[A]dd [E]dit [D]el [Q]uit"[:left_width])
    
    def draw_right_pane(self, stdscr, height, width):
        left_width = width // 3
        right_x = left_width + 1
        right_width = width - left_width - 1
        
        # Vertical separator
        for y in range(height):
            stdscr.addstr(y, left_width, "│")
        
        papers = self.storage.get_papers()
        if not papers:
            stdscr.addstr(0, right_x, "═" * (right_width - 1))
            stdscr.addstr(0, right_x + 2, " WELCOME ")
            stdscr.addstr(1, right_x, "═" * (right_width - 1))
            stdscr.addstr(3, right_x + 2, "Press [A] to add your first paper")
            return
        
        paper = papers[self.selected_paper]
        
        # Header
        stdscr.addstr(0, right_x, "═" * (right_width - 1))
        stdscr.addstr(0, right_x + 2, f" {paper.get_short_title()} ")
        stdscr.addstr(1, right_x, "═" * (right_width - 1))
        
        # Sections
        y = 3
        sections = [
            ("OBJECTIVE", paper.objective, "1"),
            ("METHODOLOGY", paper.methodology, "2"),
            ("CONCLUSION", paper.conclusion, "3")
        ]
        
        for section_name, section_data, key in sections:
            if y >= height - 3:
                break
            
            page_ref = f"[p.{section_data['page']}]" if section_data['page'] else ""
            header = f"┌─ {section_name} {page_ref} "
            header += "─" * (right_width - len(header) - 2) + "┐"
            stdscr.addstr(y, right_x, header[:right_width-1])
            y += 1
            
            if section_data['content']:
                lines = section_data['content'].split('\n')
                for line in lines[:3]:  # Show first 3 lines
                    if y >= height - 3:
                        break
                    display_line = f"│ {line}"
                    display_line += " " * (right_width - len(display_line) - 2) + "│"
                    stdscr.addstr(y, right_x, display_line[:right_width-1])
                    y += 1
            else:
                empty_line = f"│ [Empty - Press {key} to edit]"
                empty_line += " " * (right_width - len(empty_line) - 2) + "│"
                stdscr.addstr(y, right_x, empty_line[:right_width-1])
                y += 1
            
            footer = "└" + "─" * (right_width - 3) + "┘"
            stdscr.addstr(y, right_x, footer[:right_width-1])
            y += 2
        
        # Footer
        stdscr.addstr(height - 2, right_x, "─" * (right_width - 1))
        stdscr.addstr(height - 1, right_x, "[1][2][3] View sections [E] Edit metadata"[:right_width-1])
    
    def add_paper_flow(self, stdscr):
        curses.echo()
        curses.curs_set(1)
        stdscr.clear()
        
        stdscr.addstr(0, 0, "ADD NEW PAPER")
        stdscr.addstr(1, 0, "=" * 40)
        
        stdscr.addstr(3, 0, "Title: ")
        title = stdscr.getstr(3, 7, 60).decode('utf-8')
        
        stdscr.addstr(5, 0, "Authors (comma separated): ")
        authors = stdscr.getstr(5, 27, 60).decode('utf-8')
        
        stdscr.addstr(7, 0, "Year: ")
        year = stdscr.getstr(7, 6, 10).decode('utf-8')
        
        stdscr.addstr(9, 0, "Publisher: ")
        publisher = stdscr.getstr(9, 11, 60).decode('utf-8')
        
        stdscr.addstr(11, 0, "DOI: ")
        doi = stdscr.getstr(11, 5, 60).decode('utf-8')
        
        if title:
            paper = Paper(title, authors, year, publisher, doi)
            self.storage.add_paper(paper)
            self.selected_paper = len(self.storage.papers) - 1
        
        curses.noecho()
        curses.curs_set(0)
    
    def edit_metadata_flow(self, stdscr):
        papers = self.storage.get_papers()
        if not papers:
            return
        
        paper = papers[self.selected_paper]
        
        curses.echo()
        curses.curs_set(1)
        stdscr.clear()
        
        stdscr.addstr(0, 0, "EDIT PAPER METADATA")
        stdscr.addstr(1, 0, "=" * 40)
        
        stdscr.addstr(3, 0, f"Title [{paper.title}]: ")
        title = stdscr.getstr(3, 23 + len(paper.title), 60).decode('utf-8') or paper.title
        
        stdscr.addstr(5, 0, f"Authors [{paper.authors}]: ")
        authors = stdscr.getstr(5, 27 + len(paper.authors), 60).decode('utf-8') or paper.authors
        
        stdscr.addstr(7, 0, f"Year [{paper.year}]: ")
        year = stdscr.getstr(7, 21 + len(paper.year), 10).decode('utf-8') or paper.year
        
        stdscr.addstr(9, 0, f"Publisher [{paper.publisher}]: ")
        publisher = stdscr.getstr(9, 31 + len(paper.publisher), 60).decode('utf-8') or paper.publisher
        
        stdscr.addstr(11, 0, f"DOI [{paper.doi}]: ")
        doi = stdscr.getstr(11, 19 + len(paper.doi), 60).decode('utf-8') or paper.doi
        
        paper.title = title
        paper.authors = authors
        paper.year = year
        paper.publisher = publisher
        paper.doi = doi
        
        self.storage.update_paper(self.selected_paper, paper)
        
        curses.noecho()
        curses.curs_set(0)
    
    def view_section(self, stdscr, section_name):
        papers = self.storage.get_papers()
        if not papers:
            return
        
        paper = papers[self.selected_paper]
        section = getattr(paper, section_name)
        
        scroll_offset = 0
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Header
            stdscr.addstr(0, 0, "═" * width)
            header = f" {section_name.upper()} - {paper.get_short_title()} "
            stdscr.addstr(0, 2, header)
            stdscr.addstr(1, 0, "═" * width)
            
            # Page reference
            page_info = f"Page: {section['page']}" if section['page'] else "Page: N/A"
            stdscr.addstr(2, 2, page_info)
            stdscr.addstr(3, 0, "─" * width)
            
            # Content
            content = section['content'] if section['content'] else "[Empty section]"
            lines = content.split('\n')
            
            display_height = height - 7
            for i, line in enumerate(lines[scroll_offset:scroll_offset + display_height]):
                if 4 + i < height - 3:
                    stdscr.addstr(4 + i, 2, line[:width-4])
            
            # Scroll indicator
            if len(lines) > display_height:
                scroll_info = f"(Line {scroll_offset + 1}-{min(scroll_offset + display_height, len(lines))} of {len(lines)})"
                stdscr.addstr(height - 3, width - len(scroll_info) - 2, scroll_info)
            
            # Footer
            stdscr.addstr(height - 2, 0, "─" * width)
            stdscr.addstr(height - 1, 0, "[I]nline edit  [V]im/nano  [P]age ref  [↑↓] Scroll  [Esc] Back"[:width])
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == 27:  # Esc
                break
            elif key == ord('i') or key == ord('I'):
                self.inline_edit_section(stdscr, section_name)
                section = getattr(paper, section_name)  # Refresh
            elif key == ord('v') or key == ord('V'):
                self.external_edit_section(stdscr, section_name)
                section = getattr(paper, section_name)  # Refresh
            elif key == ord('p') or key == ord('P'):
                self.edit_page_reference(stdscr, section_name)
                section = getattr(paper, section_name)  # Refresh
            elif key == curses.KEY_UP:
                scroll_offset = max(0, scroll_offset - 1)
            elif key == curses.KEY_DOWN:
                scroll_offset = min(len(lines) - display_height, scroll_offset + 1)
                scroll_offset = max(0, scroll_offset)
    
    def inline_edit_section(self, stdscr, section_name):
        papers = self.storage.get_papers()
        paper = papers[self.selected_paper]
        section = getattr(paper, section_name)
        
        curses.echo()
        curses.curs_set(1)
        stdscr.clear()
        
        stdscr.addstr(0, 0, f"INLINE EDIT - {section_name.upper()}")
        stdscr.addstr(1, 0, "=" * 60)
        stdscr.addstr(2, 0, "Enter content (empty line to finish):")
        stdscr.addstr(3, 0, "-" * 60)
        
        # Pre-fill existing content
        lines = section['content'].split('\n') if section['content'] else []
        
        y = 4
        for line in lines:
            if y < 20:
                stdscr.addstr(y, 0, f"> {line}")
                y += 1
        
        # Continue editing
        while y < 20:
            stdscr.addstr(y, 0, "> ")
            line = stdscr.getstr(y, 2, 70).decode('utf-8')
            if not line and lines:  # Empty line = done
                break
            if line:
                lines.append(line)
            y += 1
        
        section['content'] = '\n'.join(lines)
        self.storage.update_paper(self.selected_paper, paper)
        
        curses.noecho()
        curses.curs_set(0)
    
    def external_edit_section(self, stdscr, section_name):
        papers = self.storage.get_papers()
        paper = papers[self.selected_paper]
        section = getattr(paper, section_name)
        
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(section['content'])
            temp_path = f.name
        
        # Detect editor
        editor = os.environ.get('EDITOR', 'notepad' if os.name == 'nt' else 'nano')
        
        # Exit curses temporarily
        curses.endwin()
        
        try:
            subprocess.call([editor, temp_path])
            
            # Read back
            with open(temp_path, 'r', encoding='utf-8') as f:
                section['content'] = f.read()
            
            self.storage.update_paper(self.selected_paper, paper)
        finally:
            os.unlink(temp_path)
            # Reinitialize curses
            stdscr.refresh()
    
    def edit_page_reference(self, stdscr, section_name):
        papers = self.storage.get_papers()
        paper = papers[self.selected_paper]
        section = getattr(paper, section_name)
        
        curses.echo()
        curses.curs_set(1)
        stdscr.clear()
        
        stdscr.addstr(0, 0, f"EDIT PAGE REFERENCE - {section_name.upper()}")
        stdscr.addstr(1, 0, "=" * 40)
        
        current = section['page'] if section['page'] else "N/A"
        stdscr.addstr(3, 0, f"Current page: {current}")
        stdscr.addstr(5, 0, "New page reference: ")
        page = stdscr.getstr(5, 20, 20).decode('utf-8')
        
        if page:
            section['page'] = page
            self.storage.update_paper(self.selected_paper, paper)
        
        curses.noecho()
        curses.curs_set(0)
    
    def delete_paper(self):
        papers = self.storage.get_papers()
        if papers:
            self.storage.delete_paper(self.selected_paper)
            self.selected_paper = max(0, min(self.selected_paper, len(self.storage.papers) - 1))

def main():
    app = ResearchApp()
    curses.wrapper(app.run)

if __name__ == "__main__":
    main()
