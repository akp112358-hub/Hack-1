
import json
import os
import sys
from datetime import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(__file__), 'journal.json')


def load_entries():
	if not os.path.exists(JOURNAL_FILE):
		return []
	with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
		try:
			return json.load(f)
		except Exception:
			return []


def save_entries(entries):
	with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
		json.dump(entries, f, ensure_ascii=False, indent=2)


def add_entry(text):
	entries = load_entries()
	entry = {
		'id': int(datetime.utcnow().timestamp() * 1000),
		'timestamp': datetime.utcnow().isoformat() + 'Z',
		'text': text,
	}
	entries.insert(0, entry)
	save_entries(entries)
	print('Added entry', entry['id'])


def list_entries():
	entries = load_entries()
	if not entries:
		print('No entries')
		return
	for e in entries:
		t = e.get('timestamp')
		text = e.get('text','')
		print(f"{e.get('id')} - {t} - {text.splitlines()[0][:80]}")


def view_entry(entry_id):
	entries = load_entries()
	for e in entries:
		if str(e.get('id')) == str(entry_id):
			print(f"ID: {e.get('id')}")
			print(f"Timestamp: {e.get('timestamp')}")
			print('---')
			print(e.get('text'))
			return
	print('Entry not found')


def delete_entry(entry_id):
	entries = load_entries()
	new = [e for e in entries if str(e.get('id')) != str(entry_id)]
	if len(new) == len(entries):
		print('Entry not found')
		return
	save_entries(new)
	print('Deleted', entry_id)


def search_entries(query):
	entries = load_entries()
	found = [e for e in entries if query.lower() in e.get('text','').lower()]
	if not found:
		print('No matches')
		return
	for e in found:
		print(f"{e.get('id')} - {e.get('timestamp')} - {e.get('text').splitlines()[0][:80]}")


def help_text():
	print('Usage: python main.py [command] [args]\n')
	print('Commands:')
	print('  add "your text"     Add a new journal entry')
	print('  list                 List entries')
	print('  view <id>            View full entry')
	print('  delete <id>          Delete entry')
	print('  search "query"      Search entries')


def main(argv):
	if len(argv) < 2:
		help_text()
		return
	cmd = argv[1].lower()
	if cmd == 'add':
		if len(argv) < 3:
			print('Provide text to add')
			return
		add_entry(' '.join(argv[2:]))
	elif cmd == 'list':
		list_entries()
	elif cmd == 'view':
		if len(argv) < 3:
			print('Provide id to view')
			return
		view_entry(argv[2])
	elif cmd == 'delete':
		if len(argv) < 3:
			print('Provide id to delete')
			return
		delete_entry(argv[2])
	elif cmd == 'search':
		if len(argv) < 3:
			print('Provide search query')
			return
		search_entries(' '.join(argv[2:]))
	else:
		help_text()


if __name__ == '__main__':
	main(sys.argv)

