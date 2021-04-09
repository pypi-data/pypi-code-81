import apikey


def test1():
    apikey.save("service1", "supersecret", filename="tmp_file1.txt")
    key = apikey.load("service1", filename="tmp_file1.txt")
    assert key == "supersecret"
