import requests
import csv
import argparse


def fetch_commits(owner, repo, branch, token, csv_file, per_page=100):
    """Fetch GitHub commits and save them to a CSV file."""
    base_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {"Authorization": f"token {token}"} if token else {}
    params = {"sha": branch, "per_page": per_page}
    all_commits = []

    page = 1
    while True:
        params["page"] = page
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            commits = response.json()
            if not commits:
                break
            all_commits.extend(commits)
            page += 1
        else:
            print("Failed to retrieve commits:", response.status_code, response.json())
            break

    if all_commits:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["SHA", "Date", "Author", "Summary", "Description"])

            for commit in all_commits:
                sha = commit["sha"]
                message = commit["commit"]["message"]
                author = commit["commit"]["author"]["name"]
                date = commit["commit"]["author"]["date"]

                # Split the message into summary and description
                message_parts = message.split("\n", 1)
                summary = message_parts[0].strip()
                description = message_parts[1].strip() if len(message_parts) > 1 else ""

                writer.writerow([sha, date, author, summary, description])

        print(f"Saved {len(all_commits)} commits to {csv_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch GitHub commits and save to CSV")
    parser.add_argument("--owner", required=True, help="GitHub repository owner")
    parser.add_argument("--repo", required=True, help="GitHub repository name")
    parser.add_argument("--branch", default="main", help="Branch name (default: main)")
    parser.add_argument(
        "--token", default=None, help="GitHub personal access token (optional)"
    )
    parser.add_argument(
        "--output",
        default="github_commits.csv",
        help="Output CSV file (default: github_commits.csv)",
    )

    args = parser.parse_args()

    fetch_commits(args.owner, args.repo, args.branch, args.token, args.output)
