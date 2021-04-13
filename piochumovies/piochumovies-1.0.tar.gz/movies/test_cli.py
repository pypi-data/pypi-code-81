from click.testing import CliRunner
from .cli import main


def test_add_without_key():
	runner = CliRunner()

	result = runner.invoke(main, ['add'],)
	assert result.exit_code == 0
	assert "You must provide your API Key first! Type 'movies key'" in result.output


def test_top_without_movies():
	runner = CliRunner()

	result = runner.invoke(main, ['top'])
	assert result.exit_code == 0
	assert "You don't have any movies" in result.output


def test_all_without_movies():
	runner = CliRunner()

	result = runner.invoke(main, ['top'])
	assert result.exit_code == 0
	assert "You don't have any movies" in result.output


def test_profitable_without_movies():
	runner = CliRunner()

	result = runner.invoke(main, ['top'])
	assert result.exit_code == 0
	assert "You don't have any movies" in result.output


def test_avg_without_movies():
	runner = CliRunner()

	result = runner.invoke(main, ['top'])
	assert result.exit_code == 0
	assert "You don't have any movies" in result.output


def test_key():
	runner = CliRunner()

	result = runner.invoke(main, ['key'], input='ba9d99de')
	assert result.exit_code == 0
	assert 'API Key added' in result.output


def test_add_should_failed():
	runner = CliRunner()

	result = runner.invoke(main, ['add'], input='asdajsdhaksjdfhskjdsdsdfsdf\n')
	assert result.exit_code == 0
	assert "Sorry :( We haven't found any movie" in result.output


def test_add():
	runner = CliRunner()

	result = runner.invoke(main, ['add'], input='The Shawshank Redemption\ny\nThe Green Mile\ny\nSeven Pounds\nn\ny')
	assert result.exit_code == 0
	assert 'Movies added' in result.output


def test_top():
	runner = CliRunner()

	result = runner.invoke(main, ['top'])
	assert result.exit_code == 0
	assert 'Here are your top 1 movies' in result.output
	assert '1. The Shawshank Redemption IMDB rating: 9.3' in result.output


def test_all():
	runner = CliRunner()

	result = runner.invoke(main, ['all'])
	assert result.exit_code == 0
	assert '1. The Shawshank Redemption' in result.output
	assert '2. The Green Mile' in result.output
	assert '3. Seven Pounds' in result.output


def test_profitable():
	runner = CliRunner()

	result = runner.invoke(main, ['profitable'])
	assert result.exit_code == 0
	assert 'Most profitable movie in you library is The Green Mile with lifetime gross = $136,801,374' in result.output


def test_avg():
	runner = CliRunner()

	result = runner.invoke(main, ['avg'])
	assert result.exit_code == 0
	assert 'Average IMDB rating of movies in your library is 8.5' in result.output