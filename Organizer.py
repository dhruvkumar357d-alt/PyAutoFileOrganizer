import os

from organizer import get_category, unique_path, organize_directory


def make_files(folder, names):
    for name in names:
        (folder / name).write_text("test")


def test_get_category_known_extensions():
    assert get_category(".pdf") == "Documents"
    assert get_category(".jpg") == "Images"
    assert get_category(".mp3") == "Audio"
    assert get_category(".zip") == "Archives"


def test_get_category_unknown_extension():
    assert get_category(".xyz") == "Others"
    assert get_category("") == "Others"


def test_unique_path_no_collision(tmp_path):
    assert unique_path(str(tmp_path), "a.txt") == str(tmp_path / "a.txt")


def test_unique_path_with_collision(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "a_1.txt").write_text("x")
    assert unique_path(str(tmp_path), "a.txt") == str(tmp_path / "a_2.txt")


def test_files_are_moved_to_categories(tmp_path):
    make_files(tmp_path, ["a.pdf", "b.jpg", "c.xyz"])
    organize_directory(str(tmp_path))
    assert (tmp_path / "Documents" / "a.pdf").exists()
    assert (tmp_path / "Images" / "b.jpg").exists()
    assert (tmp_path / "Others" / "c.xyz").exists()


def test_dry_run_changes_nothing(tmp_path):
    make_files(tmp_path, ["a.pdf"])
    organize_directory(str(tmp_path), dry_run=True)
    assert (tmp_path / "a.pdf").exists()
    assert not (tmp_path / "Documents").exists()


def test_existing_files_are_not_overwritten(tmp_path):
    (tmp_path / "Documents").mkdir()
    (tmp_path / "Documents" / "a.pdf").write_text("old")
    (tmp_path / "a.pdf").write_text("new")
    organize_directory(str(tmp_path))
    assert (tmp_path / "Documents" / "a.pdf").read_text() == "old"
    assert (tmp_path / "Documents" / "a_1.pdf").read_text() == "new"


def test_hidden_files_and_folders_are_skipped(tmp_path):
    make_files(tmp_path, [".hidden"])
    (tmp_path / "subfolder").mkdir()
    organize_directory(str(tmp_path))
    assert (tmp_path / ".hidden").exists()
    assert (tmp_path / "subfolder").is_dir()


def test_invalid_path_does_not_crash():
    organize_directory("this/path/does/not/exist")
