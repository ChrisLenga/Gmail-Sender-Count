import os
import pickle
from collections import Counter
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete token.pickle
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
TOKEN_PATH = 'token.pickle'
CREDS_PATH = 'credentials.json'
USER_ID = 'me'

def get_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)
    return build('gmail', 'v1', credentials=creds)

def list_message_ids(service, query=''):
    """Return list of all message ids matching the Gmail query."""
    ids = []
    resp = service.users().messages().list(userId=USER_ID, q=query).execute()
    while resp and 'messages' in resp:
        ids += [m['id'] for m in resp['messages']]
        if 'nextPageToken' in resp:
            resp = service.users().messages().list(
                userId=USER_ID,
                q=query,
                pageToken=resp['nextPageToken']
            ).execute()
        else:
            break
    return ids

def get_sender_for_message(service, msg_id):
    """Fetch the From header for a single message id."""
    msg = service.users().messages().get(
        userId=USER_ID,
        id=msg_id,
        format='metadata',
        metadataHeaders=['From']
    ).execute()
    headers = msg.get('payload', {}).get('headers', [])
    for h in headers:
        if h['name'] == 'From':
            return h['value']
    return None

def count_senders(service, query=''):
    """Return Counter of senders for all messages matching query."""
    ids = list_message_ids(service, query)
    cnt = Counter()
    for i, msg_id in enumerate(ids, 1):
        sender = get_sender_for_message(service, msg_id)
        if sender:
            cnt[sender] += 1
        if i % 200 == 0:
            print(f'processed {i}/{len(ids)}')
    return cnt

def delete_messages_from_sender(service, sender, query=''):
    """
    Mass‑delete (move to trash) every message from a given sender.
    Optionally refine with extra query (e.g. date range).
    """
    full_query = f'from:{sender} {query}'.strip()
    ids = list_message_ids(service, full_query)
    print(f'going to delete {len(ids)} messages from {sender}')
    # Gmail API batchDelete accepts up to 1000 ids per request
    for i in range(0, len(ids), 1000):
        chunk = ids[i:i+1000]
        service.users().messages().batchDelete(
            userId=USER_ID,
            body={'ids': chunk}
        ).execute()

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Count or delete Gmail by sender')
    p.add_argument('--query', default='', help='Gmail search query to narrow messages')
    p.add_argument('--count', action='store_true', help='Just show counts per sender')
    p.add_argument('--delete', metavar='SENDER_EMAIL', help=' mass delete messages from this sender')
    args = p.parse_args()

    svc = get_service()

    if args.count:
        stats = count_senders(svc, args.query)
        for sender, n in stats.most_common():
            print(f'{n:6d}  {sender}')
    elif args.delete:
        delete_messages_from_sender(svc, args.delete, args.query)
        print('done')
    else:
        print('nothing done  use --count or --delete')

