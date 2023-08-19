class Paginator:
    def __init__(self, items: list, page_size: int):
        self.items = items
        self.page_size = page_size
        self.curr_page = 1
        self.curr_index = 0
        self.total_pages = len(self.items) // self.page_size + 1

    def get_page(self):
        return self.items[self.curr_index:self.curr_index+self.page_size]
    
    def next_page(self):
        if self.curr_index + self.page_size < len(self.items):
            self.curr_index += self.page_size
            self.curr_page += 1
            return self.get_page()
        return None
    
    def prev_page(self):
        if self.curr_index - self.page_size >= 0:
            self.curr_index -= self.page_size
            self.curr_page -= 1
            return self.get_page()
        return None