#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

class DiaryImpl {
public:
    DiaryImpl(const std::string &content, int m = 0, int d = 0)
        : content(content), month(m), day(d) 
    {
        if (m == 0 && d == 0) {
            throw std::runtime_error("Invalid date");
        }

        lines = 1;
        words = 0;
        bool in_word = false;
        for (char c : content) {
            if (c == '\n')
                lines++;
            if (c == ' ' || c == '\n' || c == '\t') {
                if (in_word) {
                    words++;
                    in_word = false;
                }
            } else {
                in_word = true;
            }
        }
        if (in_word) {
            words++;
        }
    }
    ~DiaryImpl() = default;

    void show() { 
        std::cout << content << "\n=======================\n" << words << " words, " << lines << " lines" << std::endl; 
    }

    void show_summary() {
        std::cout << "Diary - " << month << "/" << day << std::endl;
    }

    void to_upper() {
        for (char &c : content) {
            c = std::toupper(c);
        }
    }

    void set_date(int m, int d) {
        month = m;
        day = d;
    }

    void set_content(const std::string &new_content) { content = new_content; }

    size_t size() const { return content.size(); }

private:
    int month;
    int day;
    int lines;
    int words;
    std::string content;
};

class Diary {
public:
    Diary(const std::string &content, int month = 0, int day = 0) {
        impl = new DiaryImpl(content, month, day);
    }

    ~Diary() { delete impl; }

    void show() { impl->show(); }

    void show_summary() { impl->show_summary(); }

    void to_upper() { impl->to_upper(); }

    void update(const std::string &new_content, int month, int day) {
        if (new_content != "") {
            impl->set_content(new_content);
        }
        impl->set_date(month, day);
    }

    size_t size() const { return impl->size(); }

private:
    DiaryImpl *impl;
};

inline std::string user_input(const char *prompt) {
    std::string input;
    std::cout << prompt;
    std::cout.flush();

    std::cin.ignore();

    char *line = nullptr;
    size_t len = 0;
    ssize_t read = getline(&line, &len, stdin);
    if (read < 0) {
        exit(1);
    }

    if (line[read - 1] == '\n') {
        line[read - 1] = '\0';
    }

    return std::string(line);
}

std::vector<Diary> diaries;

void create() {
    int month, day;
    std::cout << "Enter date (month day): ";
    std::cout.flush();
    std::cin >> month >> day;

    std::string content = user_input("Enter diary content: ");

    diaries.emplace_back(content, month, day);
}

void show_with_emphasis(Diary diary) {
    diary.to_upper();
    diary.show();
}

void show(bool formatted = false) {
    int index;
    std::cout << "Enter diary index: ";
    std::cout.flush();
    std::cin >> index;

    if (index >= 0 && index < diaries.size()) {
        if (formatted) {
            show_with_emphasis(diaries[index]);
        } else {
            diaries[index].show();
        }
    } else {
        std::cout << "Invalid index." << std::endl;
    }
}

void update() {
    int index;
    std::cout << "Enter diary index to update: ";
    std::cout.flush();
    std::cin >> index;

    if (index >= 0 && index < diaries.size()) {
        int month, day;
        std::cout << "Enter new date (month day): ";
        std::cout.flush();
        std::cin >> month >> day;

        std::string content = user_input("Enter new diary content: ");

        diaries[index].update(content, month, day);
        std::cout << "Diary updated." << std::endl;
    } else {
        std::cout << "Invalid index." << std::endl;
    }
}

void list_diaries() {
    std::cout << "Diaries:" << std::endl;
    for (size_t i = 0; i < diaries.size(); ++i) {
        std::cout << i << ": ";
        diaries[i].show_summary();
    }
    std::cout.flush();
}

int main() {
    diaries.reserve(64);

    while (true) {
        std::cout << "1. Create Diary\n"
                     "2. Show Diary\n"
                     "3. Show Diary with Emphasis\n"
                     "4. Update Diary\n"
                     "5. List Diaries\n"
                     "6. Exit\n"
                     "Enter your choice: ";
        std::cout.flush();

        int choice;
        std::cin >> choice;

        std::cout << std::endl;

        switch (choice) {
            case 1:
                create();
                break;
            case 2:
                show(false);
                break;
            case 3:
                show(true);
                break;
            case 4:
                update();
                break;
            case 5:
                list_diaries();
                break;
            case 6:
                std::cout << "Exiting..." << std::endl;
                return 0;
            default:
                std::cout << "Invalid choice." << std::endl;
                return 0;
        }

        std::cout << std::endl;
    }

    return 0;
}
