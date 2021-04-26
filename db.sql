
CREATE SEQUENCE public.categorylist_cat_id_seq;

CREATE TABLE public.Categorylist (
                cat_id INTEGER NOT NULL DEFAULT nextval('public.categorylist_cat_id_seq'),
                CategoryName VARCHAR NOT NULL,
                Des VARCHAR NOT NULL,
                CONSTRAINT categorylist_pk PRIMARY KEY (cat_id)
);


ALTER SEQUENCE public.categorylist_cat_id_seq OWNED BY public.Categorylist.cat_id;

CREATE TABLE public.Student (
                std_id BIGINT NOT NULL,
                std_firstname VARCHAR NOT NULL,
                std_lastname VARCHAR NOT NULL,
                std_major VARCHAR NOT NULL,
                std_year VARCHAR NOT NULL,
                CONSTRAINT student_pk PRIMARY KEY (std_id)
);


CREATE SEQUENCE public.borrower_borrower_id_seq;

CREATE TABLE public.Borrower (
                Borrower_id INTEGER NOT NULL DEFAULT nextval('public.borrower_borrower_id_seq'),
                ReturnDate VARCHAR NOT NULL,
                BorrowerDate VARCHAR NOT NULL,
                std_id BIGINT NOT NULL,
                CONSTRAINT borrower_pk PRIMARY KEY (Borrower_id)
);


ALTER SEQUENCE public.borrower_borrower_id_seq OWNED BY public.Borrower.Borrower_id;

CREATE SEQUENCE public.author_author_id_seq_1;

CREATE TABLE public.Author (
                author_id INTEGER NOT NULL DEFAULT nextval('public.author_author_id_seq_1'),
                author_firstname VARCHAR NOT NULL,
                author_lastname VARCHAR NOT NULL,
                CONSTRAINT author_pk PRIMARY KEY (author_id)
);


ALTER SEQUENCE public.author_author_id_seq_1 OWNED BY public.Author.author_id;

CREATE SEQUENCE public.book_book_id_seq;

CREATE TABLE public.Book (
                Book_id INTEGER NOT NULL DEFAULT nextval('public.book_book_id_seq'),
                Booktitle VARCHAR NOT NULL,
                floor VARCHAR NOT NULL,
                book_publisher VARCHAR NOT NULL,
                stock INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                CONSTRAINT book_pk PRIMARY KEY (Book_id)
);


ALTER SEQUENCE public.book_book_id_seq OWNED BY public.Book.Book_id;

CREATE TABLE public.Category (
                Book_id INTEGER NOT NULL,
                cat_id INTEGER NOT NULL
);


CREATE TABLE public.Borrowers_books (
                Book_id INTEGER NOT NULL,
                Borrower_id INTEGER NOT NULL
);


ALTER TABLE public.Category ADD CONSTRAINT category_list_category_fk
FOREIGN KEY (cat_id)
REFERENCES public.Categorylist (cat_id)
ON DELETE CASCADE
ON UPDATE CASCADE
NOT DEFERRABLE;

ALTER TABLE public.Borrower ADD CONSTRAINT student_borrower_fk
FOREIGN KEY (std_id)
REFERENCES public.Student (std_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.Borrowers_books ADD CONSTRAINT borrower_borrowers_books_fk
FOREIGN KEY (Borrower_id)
REFERENCES public.Borrower (Borrower_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.Book ADD CONSTRAINT author_book_fk
FOREIGN KEY (author_id)
REFERENCES public.Author (author_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.Borrowers_books ADD CONSTRAINT book_borrowers_books_fk
FOREIGN KEY (Book_id)
REFERENCES public.Book (Book_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.Category ADD CONSTRAINT book_category_fk
FOREIGN KEY (Book_id)
REFERENCES public.Book (Book_id)
ON DELETE CASCADE
ON UPDATE CASCADE
NOT DEFERRABLE;

ต้อง INSERT  