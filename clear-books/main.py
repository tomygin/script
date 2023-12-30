import hashlib
import os


class Book:
    name: str
    suffix: str
    content_md5: str
    absolute_path: str

    def __init__(self, name, suffix, content_md5, absolute_path):
        self.name = name
        self.suffix = suffix
        self.content_md5 = content_md5
        self.absolute_path = absolute_path

    def __str__(self):
        return f"name:{self.name}\nsuffix:{self.suffix}\ncontent_md5:{self.content_md5}\nabsolute_path:{self.absolute_path}\n--------"


# 读取dir_path目录下所有文件
def read_dir(dir_path):
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


# 将读取的所有文件转化为Book对象
def convert_to_book(file_list):
    book_list = []
    for file in file_list:
        name = os.path.basename(file)
        # 获取文件后缀名
        suffix = os.path.splitext(file)[1]
        # 读取文件内容然后计算得出md5
        with open(file, "rb") as f:
            content = f.read()
            content_md5 = hashlib.md5(content).hexdigest()
        absolute_path = os.path.abspath(file)
        book = Book(name, suffix, content_md5, absolute_path)
        book_list.append(book)
    return book_list


# 去除book_list中重复的book
def remove_duplicate(book_list):
    book_dict = {}
    for book in book_list:
        book_dict[book.content_md5] = book
    return list(book_dict.values())


# 对book_list进行排序
def sort_book(book_list, order_by):
    return sorted(book_list, key=lambda x: order_by.index(x.suffix))


#保留book_list中的书籍不被移动，其他书籍全部移动到new_dir_path
def move_file(move_book_list, new_dir_path):
    #如果new_dir_path不存在，则创建
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

    for book in move_book_list:
        new_file_path = os.path.join(new_dir_path, book.name)
        os.rename(book.absolute_path, new_file_path)


if __name__ == '__main__':

    # --------
    #需要配置的清单
    dir_path = ".\\clear-books\\books"
    new_dir_path = ".\\clear-books\\new-books"
    order_by = ['.epub', '.mobi', '.pdf', '.txt']
    # --------

    file_list = read_dir(dir_path)
    all_book_list = convert_to_book(file_list)
    book_list = remove_duplicate(all_book_list)
    book_list = sort_book(book_list, order_by)

    for book in book_list:
        print(book)

    # 需要移动的书籍
    move_book_list = []
    for book in all_book_list:
        flag = False
        for _book in book_list:
            if book.absolute_path == _book.absolute_path:
                flag = True
        if not flag:
            move_book_list.append(book)

    print("will move books:")
    for book in move_book_list:
        print(book)
    move_file(move_book_list, new_dir_path)
