import os
import requests

def test_something():
	"""Run some automated tests"""
	test_passed = True
	# content of your test goes here, update 'test_passed' accordingly

	if test_passed:
		return 0, "The test passed!"
	else:
		return 1, "Uh oh, the test failed!"

def add_github_comment(result, message):
	"""
	Add a comment to a Pull Request in GitHub
		:result: (int) exit code of tests, 0 is pass, 1 is fail
		:message: (str) the content of the Pull Request comment
	"""
	travis_pull_request = os.environ.get('TRAVIS_PULL_REQUEST')
	user = "YOUR GITHUB USERNAME"
	repo = "YOUR GITHUB REPOSITORY NAME"

	GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
	headers = { 'Authorization': f'token {GITHUB_TOKEN}' }
	content = f'{{"body":"{message}"}}'
	response = requests.post(
		f'https://api.github.com/repos/{user}/{repo}/issues/{travis_pull_request}/comments',
		headers=headers,
		data=content.encode('utf-8')
	)

def main():
	result, message = test_something()
	add_github_comment(result, message)

if __name__ == '__main__':
	main()