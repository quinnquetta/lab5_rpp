import os
import csv


class Post:
    def __init__(self, post_id: int, nickname: str, text: str, likes: int):
        self.post_id = post_id
        self.nickname = nickname
        self.text = text
        self.likes = likes

    def __setattr__(self, name, value):
        if name in ('post_id', 'likes'):
            value = int(value)
        object.__setattr__(self, name, value)

    def __repr__(self):
        return f"Post(id={self.post_id}, nick='{self.nickname}', text='{self.text}', likes={self.likes})"


class SponsoredPost(Post):
    def __init__(self, post_id: int, nickname: str, text: str, likes: int, sponsor: str):
        super().__init__(post_id, nickname, text, likes)
        self.sponsor = sponsor

    def __setattr__(self, name, value):
        if name == 'sponsor':
            value = str(value)
        super().__setattr__(name, value)

    def __repr__(self):
        return f"SponsoredPost(id={self.post_id}, nick='{self.nickname}', text='{self.text}', likes={self.likes}, sponsor='{self.sponsor}')"


class PostCollection:
    def __init__(self):
        self._posts = []
        self._index = 0

    def add_post(self, post: Post):
        self._posts.append(post)

    def __getitem__(self, index):
        return self._posts[index]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._posts):
            item = self._posts[self._index]
            self._index += 1
            return item
        raise StopIteration

    def get_popular_posts(self, min_likes: int):
        for post in self._posts:
            if post.likes > min_likes:
                yield post

    @staticmethod
    def count_files(directory: str) -> int:
        try:
            return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        except FileNotFoundError:
            return 0

    def sort_by_nickname(self):
        self._posts.sort(key=lambda p: p.nickname)

    def sort_by_likes(self):
        self._posts.sort(key=lambda p: p.likes, reverse=True)

    def save_to_csv(self, filename: str):
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['type', 'id', 'nickname', 'text', 'likes', 'sponsor'])
            for p in self._posts:
                if isinstance(p, SponsoredPost):
                    writer.writerow(['sponsored', p.post_id, p.nickname, p.text, p.likes, p.sponsor])
                else:
                    writer.writerow(['standard', p.post_id, p.nickname, p.text, p.likes, ''])

    def load_from_csv(self, filename: str):
        self._posts.clear()
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    p_type = row.get('type', 'standard')
                    pid = int(row['id'])
                    nick = row['nickname']
                    text = row['text']
                    likes = int(row['likes'])
                    if p_type == 'sponsored':
                        self.add_post(SponsoredPost(pid, nick, text, likes, row['sponsor']))
                    else:
                        self.add_post(Post(pid, nick, text, likes))
        except FileNotFoundError:
            pass


def main():
    directory = input("Введите путь к директории для подсчета файлов: ")
    print(f"Количество файлов в директории: {PostCollection.count_files(directory)}")

    collection = PostCollection()
    filename = 'data_oop.csv'

    if not os.path.exists(filename):
        collection.add_post(Post(1, 'user_alpha', 'Привет, мир!', 15))
        collection.add_post(SponsoredPost(2, 'admin', 'Реклама продукта', 120, 'TechCorp'))
        collection.add_post(Post(3, 'guest99', 'Вопрос по коду', 2))
        collection.save_to_csv(filename)
    else:
        collection.load_from_csv(filename)

    print("\nИсходные данные (итератор):")
    for post in collection:
        print(post)

    print("\nДоступ по индексу collection[1]:")
    if len(collection._posts) > 1:
        print(collection[1])

    print("\nСортировка по нику:")
    collection.sort_by_nickname()
    for post in collection:
        print(post)

    print("\nСортировка по лайкам (по убыванию):")
    collection.sort_by_likes()
    for post in collection:
        print(post)

    try:
        min_likes = int(input("\nВведите минимальное количество лайков для фильтрации: "))
        print("\nОтфильтрованные данные (генератор):")
        for popular_post in collection.get_popular_posts(min_likes):
            print(popular_post)
    except ValueError:
        print("Некорректный ввод числа.")

    print("\nДобавление нового поста:")
    try:
        new_id = len(collection._posts) + 1
        nick = input("Введите ник: ")
        text = input("Введите текст: ")
        likes = int(input("Введите лайки: "))
        is_sponsored = input("Это спонсорский пост? (y/n): ").strip().lower()

        if is_sponsored == 'y':
            sponsor = input("Введите название спонсора: ")
            collection.add_post(SponsoredPost(new_id, nick, text, likes, sponsor))
        else:
            collection.add_post(Post(new_id, nick, text, likes))

        collection.save_to_csv(filename)
        print("Новые данные успешно сохранены.")
    except ValueError:
        print("Ошибка ввода. Лайки должны быть числом.")


if __name__ == "__main__":
    main()
# Конец программы