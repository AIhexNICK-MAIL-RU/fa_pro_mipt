-- Очищаем таблицы (если они уже существуют)
TRUNCATE TABLE ratings, track, "user" RESTART IDENTITY CASCADE;

-- 1. Создаем 16 случайных пользователей
INSERT INTO "user" (login, first_name, last_name, email, hashed_password)
VALUES
    ('user1', 'Иван', 'Иванов', 'ivan@example.com', 'hashed_pass_1'),
    ('user2', 'Петр', 'Петров', 'petr@example.com', 'hashed_pass_2'),
    ('user3', 'Анна', 'Сидорова', 'anna@example.com', 'hashed_pass_3'),
    ('user4', 'Мария', 'Кузнецова', 'maria@example.com', 'hashed_pass_4'),
    ('user5', 'Алексей', 'Смирнов', 'alex@example.com', 'hashed_pass_5'),
    ('user6', 'Елена', 'Попова', 'elena@example.com', 'hashed_pass_6'),
    ('user7', 'Дмитрий', 'Васильев', 'dmitry@example.com', 'hashed_pass_7'),
    ('user8', 'Ольга', 'Новикова', 'olga@example.com', 'hashed_pass_8'),
    ('user9', 'Сергей', 'Федоров', 'sergey@example.com', 'hashed_pass_9'),
    ('user10', 'Татьяна', 'Морозова', 'tanya@example.com', 'hashed_pass_10'),
    ('user11', 'Андрей', 'Волков', 'andrey@example.com', 'hashed_pass_11'),
    ('user12', 'Наталья', 'Алексеева', 'natalia@example.com', 'hashed_pass_12'),
    ('user13', 'Артем', 'Лебедев', 'artem@example.com', 'hashed_pass_13'),
    ('user14', 'Виктория', 'Семенова', 'vika@example.com', 'hashed_pass_14'),
    ('user15', 'Михаил', 'Павлов', 'misha@example.com', 'hashed_pass_15'),
   	('root', 'Админ', 'Админ', 'root@example.com', 'hashed_pass_14');

-- 2. Создаем 50 случайных фильмов с разными жанрами
INSERT INTO movie (title, director, genre)
VALUES
    ('The Last Sunset', 'Christopher Nolan', 'Sci-Fi'),
    ('Midnight Whispers', 'David Fincher', 'Thriller'),
    ('Eternal Echoes', 'Denis Villeneuve', 'Drama'),
    ('Crimson Horizon', 'Quentin Tarantino', 'Action'),
    ('Silent Shadows', 'Alfred Hitchcock', 'Mystery'),
    ('Neon Dreams', 'Nicolas Winding Refn', 'Noir'),
    ('The Forgotten Kingdom', 'Peter Jackson', 'Fantasy'),
    ('Laughing in the Rain', 'Woody Allen', 'Comedy'),
    ('Sapphire Skies', 'Ridley Scott', 'Adventure'),
    ('The Hollow Crown', 'Kenneth Branagh', 'Historical'),
    ('Whispers of the Heart', 'Hayao Miyazaki', 'Animation'),
    ('Blackout', 'Martin Scorsese', 'Crime'),
    ('The Last Voyage', 'James Cameron', 'Action'),
    ('Frozen Memories', 'Lars von Trier', 'Drama'),
    ('Electric Dreams', 'Spike Jonze', 'Sci-Fi'),
    ('The Silver Lining', 'Wes Anderson', 'Comedy'),
    ('Blood and Roses', 'Park Chan-wook', 'Horror'),
    ('The Silent Witness', 'Roman Polanski', 'Thriller'),
    ('Starlight Serenade', 'Damien Chazelle', 'Musical'),
    ('The Iron Mask', 'Guy Ritchie', 'Adventure'),
    ('Shadows of the Past', 'Paul Thomas Anderson', 'Drama'),
    ('The Clockwork Prince', 'Tim Burton', 'Fantasy'),
    ('City of Mirrors', 'Bong Joon-ho', 'Mystery'),
    ('The Golden Key', 'Steven Spielberg', 'Adventure'),
    ('Echoes of War', 'Clint Eastwood', 'War'),
    ('The Phantom Rhapsody', 'Guillermo del Toro', 'Fantasy'),
    ('Midnight in Paris', 'Woody Allen', 'Romance'),
    ('The Darkest Hour', 'Joe Wright', 'Historical'),
    ('The Last Laugh', 'Charlie Chaplin', 'Comedy'),
    ('The Forgotten Symphony', 'Darren Aronofsky', 'Drama'),
    ('The Crimson Tide', 'Tony Scott', 'Action'),
    ('The Silent Storm', 'Andrea Arnold', 'Drama'),
    ('The Neon Phantom', 'Nicolas Winding Refn', 'Noir'),
    ('The Lost Treasure', 'Robert Zemeckis', 'Adventure'),
    ('The Hollow Man', 'David Cronenberg', 'Horror'),
    ('The Last Waltz', 'Martin Scorsese', 'Documentary'),
    ('The Glass Key', 'Coen Brothers', 'Crime'),
    ('The Silver Bullet', 'Sam Raimi', 'Horror'),
    ('The Forgotten Island', 'Steven Spielberg', 'Adventure'),
    ('The Shadow Dancer', 'Luc Besson', 'Action'),
    ('The Final Curtain', 'Billy Wilder', 'Drama'),
    ('The Clockwork Girl', 'Jean-Pierre Jeunet', 'Fantasy'),
    ('The Crimson Mask', 'Akira Kurosawa', 'Historical'),
    ('The Last Goodbye', 'Richard Linklater', 'Romance'),
    ('The Silent Sea', 'Bong Joon-ho', 'Sci-Fi'),
    ('The Electric Circus', 'Danny Boyle', 'Drama'),
    ('The Golden Compass', 'Chris Weitz', 'Fantasy'),
    ('The Darkest Night', 'John Carpenter', 'Horror'),
    ('The Forgotten Road', 'Wim Wenders', 'Drama'),
    ('The Phantom Opera', 'Joel Schumacher', 'Musical'),
    ('The Last Emperor', 'Bernardo Bertolucci', 'Historical');

-- 3. Создаем 150 уникальных оценок с учетом ограничений
DO $$
DECLARE
    i INTEGER := 0;
    selected_user_id INTEGER;
    selected_track_id INTEGER;
    estimate INTEGER;
    track_genre TEXT;
BEGIN
    WHILE i < 150 LOOP
        -- Выбираем случайного пользователя и трек
        selected_user_id := 1 + floor(random() * 15);
        selected_track_id := 1 + floor(random() * 50);
        
        -- Проверяем, нет ли уже такой оценки (используем явные имена таблиц)
        PERFORM 1 FROM public.ratings 
        WHERE user_id = selected_user_id AND track_id = selected_track_id;
        IF NOT FOUND THEN
            -- Базовый рейтинг (70% высоких оценок)
            IF random() < 0.7 THEN
                estimate := 4 + floor(random() * 2); -- 4 или 5
            ELSE
                estimate := 1 + floor(random() * 3); -- 1, 2 или 3
            END IF;
            
            -- Получаем жанр трека
            SELECT genre INTO track_genre FROM public.track WHERE id = selected_track_id;
            
            -- Учитываем жанровые предпочтения
            IF selected_user_id <= 5 AND track_genre = 'Rock' THEN
                estimate := LEAST(5, estimate + 1);
            ELSIF selected_user_id BETWEEN 6 AND 10 AND track_genre = 'Pop' THEN
                estimate := LEAST(5, estimate + 1);
            ELSIF selected_user_id >= 11 AND track_genre = 'Jazz' THEN
                estimate := LEAST(5, estimate + 1);
            END IF;
            
            -- Вставляем оценку
            INSERT INTO public.ratings (user_id, track_id, estimate)
            VALUES (selected_user_id, selected_track_id, estimate);
            
            i := i + 1;
        END IF;
    END LOOP;
END $$;

-- Проверяем количество созданных оценок (должно быть 150)
SELECT COUNT(*) FROM ratings;

-- Проверяем отсутствие дубликатов
SELECT user_id, track_id, COUNT(*) 
FROM ratings 
GROUP BY user_id, track_id 
HAVING COUNT(*) > 1;