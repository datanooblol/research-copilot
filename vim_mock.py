import curses

class VimMock:
    def __init__(self, initial_text=""):
        self.lines = initial_text.split('\n') if initial_text else [""]
        self.cursor_y = 0
        self.cursor_x = 0
        self.mode = "NORMAL"  # NORMAL, INSERT
        self.scroll_offset = 0
        self.message = ""
    
    def run(self, stdscr):
        curses.curs_set(1)
        stdscr.clear()
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Draw content
            display_height = height - 2
            for i in range(display_height):
                line_num = self.scroll_offset + i
                if line_num < len(self.lines):
                    line = self.lines[line_num][:width-1]
                    stdscr.addstr(i, 0, line)
            
            # Status bar
            status = f" {self.mode} | Line {self.cursor_y + 1}/{len(self.lines)} Col {self.cursor_x + 1} "
            stdscr.addstr(height - 2, 0, " " * (width - 1), curses.A_REVERSE)
            stdscr.addstr(height - 2, 0, status[:width-1], curses.A_REVERSE)
            
            # Message bar
            if self.message:
                stdscr.addstr(height - 1, 0, self.message[:width-1])
            
            # Position cursor
            screen_y = self.cursor_y - self.scroll_offset
            if 0 <= screen_y < display_height:
                stdscr.move(screen_y, min(self.cursor_x, len(self.lines[self.cursor_y])))
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            self.message = ""
            
            if self.mode == "NORMAL":
                if key == ord('q'):
                    return '\n'.join(self.lines)
                elif key == ord('i'):
                    self.mode = "INSERT"
                    self.message = "-- INSERT --"
                elif key == ord('a'):
                    self.cursor_x = min(self.cursor_x + 1, len(self.lines[self.cursor_y]))
                    self.mode = "INSERT"
                    self.message = "-- INSERT --"
                elif key == ord('o'):
                    self.lines.insert(self.cursor_y + 1, "")
                    self.cursor_y += 1
                    self.cursor_x = 0
                    self.mode = "INSERT"
                    self.message = "-- INSERT --"
                elif key == ord('O'):
                    self.lines.insert(self.cursor_y, "")
                    self.cursor_x = 0
                    self.mode = "INSERT"
                    self.message = "-- INSERT --"
                elif key == ord('x'):
                    if self.cursor_x < len(self.lines[self.cursor_y]):
                        line = self.lines[self.cursor_y]
                        self.lines[self.cursor_y] = line[:self.cursor_x] + line[self.cursor_x + 1:]
                elif key == ord('d'):
                    next_key = stdscr.getch()
                    if next_key == ord('d'):  # dd - delete line
                        if len(self.lines) > 1:
                            self.lines.pop(self.cursor_y)
                            self.cursor_y = min(self.cursor_y, len(self.lines) - 1)
                        else:
                            self.lines = [""]
                        self.cursor_x = 0
                elif key == ord('h') or key == curses.KEY_LEFT:
                    self.cursor_x = max(0, self.cursor_x - 1)
                elif key == ord('l') or key == curses.KEY_RIGHT:
                    self.cursor_x = min(len(self.lines[self.cursor_y]), self.cursor_x + 1)
                elif key == ord('j') or key == curses.KEY_DOWN:
                    if self.cursor_y < len(self.lines) - 1:
                        self.cursor_y += 1
                        self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
                        self.adjust_scroll(height - 2)
                elif key == ord('k') or key == curses.KEY_UP:
                    if self.cursor_y > 0:
                        self.cursor_y -= 1
                        self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
                        self.adjust_scroll(height - 2)
                elif key == ord('0'):
                    self.cursor_x = 0
                elif key == ord('$'):
                    self.cursor_x = len(self.lines[self.cursor_y])
                elif key == ord('g'):
                    next_key = stdscr.getch()
                    if next_key == ord('g'):  # gg - go to top
                        self.cursor_y = 0
                        self.cursor_x = 0
                        self.scroll_offset = 0
                elif key == ord('G'):  # G - go to bottom
                    self.cursor_y = len(self.lines) - 1
                    self.cursor_x = 0
                    self.adjust_scroll(height - 2)
            
            elif self.mode == "INSERT":
                if key == 27:  # Esc
                    self.mode = "NORMAL"
                    self.cursor_x = max(0, self.cursor_x - 1)
                elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                    if self.cursor_x > 0:
                        line = self.lines[self.cursor_y]
                        self.lines[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
                        self.cursor_x -= 1
                    elif self.cursor_y > 0:
                        # Join with previous line
                        prev_line = self.lines[self.cursor_y - 1]
                        curr_line = self.lines[self.cursor_y]
                        self.lines[self.cursor_y - 1] = prev_line + curr_line
                        self.lines.pop(self.cursor_y)
                        self.cursor_y -= 1
                        self.cursor_x = len(prev_line)
                elif key == curses.KEY_ENTER or key == 10 or key == 13:
                    line = self.lines[self.cursor_y]
                    self.lines[self.cursor_y] = line[:self.cursor_x]
                    self.lines.insert(self.cursor_y + 1, line[self.cursor_x:])
                    self.cursor_y += 1
                    self.cursor_x = 0
                    self.adjust_scroll(height - 2)
                elif key == curses.KEY_LEFT:
                    self.cursor_x = max(0, self.cursor_x - 1)
                elif key == curses.KEY_RIGHT:
                    self.cursor_x = min(len(self.lines[self.cursor_y]), self.cursor_x + 1)
                elif key == curses.KEY_UP:
                    if self.cursor_y > 0:
                        self.cursor_y -= 1
                        self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
                        self.adjust_scroll(height - 2)
                elif key == curses.KEY_DOWN:
                    if self.cursor_y < len(self.lines) - 1:
                        self.cursor_y += 1
                        self.cursor_x = min(self.cursor_x, len(self.lines[self.cursor_y]))
                        self.adjust_scroll(height - 2)
                elif 32 <= key <= 126:  # Printable characters
                    line = self.lines[self.cursor_y]
                    self.lines[self.cursor_y] = line[:self.cursor_x] + chr(key) + line[self.cursor_x:]
                    self.cursor_x += 1
    
    def adjust_scroll(self, display_height):
        if self.cursor_y < self.scroll_offset:
            self.scroll_offset = self.cursor_y
        elif self.cursor_y >= self.scroll_offset + display_height:
            self.scroll_offset = self.cursor_y - display_height + 1

def edit_text(initial_text=""):
    """Entry point to edit text with vim-like interface"""
    editor = VimMock(initial_text)
    return curses.wrapper(editor.run)

if __name__ == "__main__":
    # Test the editor
    result = edit_text("Hello World\nThis is a vim-like editor\nTry it out!")
    print("\n=== Final text ===")
    print(result)
