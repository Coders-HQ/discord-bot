class Paginator:
    def __init__(self, items: list, page_size: int):
        self.items = items
        self.page_size = page_size
        self.curr_page = 1 # For user-end
        self.curr_index = 0 # For back-end
        self.total_pages = len(self.items) // self.page_size + 1 # For user-end as well

    def get_page(self) -> list:
        """
        Returns the items of the current page
        """
        return self.items[self.curr_index:self.curr_index+self.page_size]
    
    def next_page(self) -> list | None:
        """
        Returns the items of the next page (None if there is no next page)
        """
        if self.curr_index + self.page_size < len(self.items):
            self.curr_index += self.page_size
            self.curr_page += 1
            return self.get_page()
        # No next page
        return None
    
    def prev_page(self) -> list | None:
        """
        Returns the items of the previous page (None if there is no previous page)
        """
        if self.curr_index - self.page_size >= 0:
            self.curr_index -= self.page_size
            self.curr_page -= 1
            return self.get_page()
        return None