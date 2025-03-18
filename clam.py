import subprocess

# TODO modify to accept multiple files and directories
def clam_scan(filename, clamAV_path):
    """
    Runs ClamAV on the specified file and returns the parsed scan results
    """

    # example clamAV path
    # clamscan_path = "/usr/bin/clamscan"
    clamscan_path = clamAV_path

    # run the clam scan on the specified file
    result = subprocess.run([clamscan_path, filename], capture_output=True, text=True)
    result = result.stdout

    SUMMARY = False
    files = []
    leftovers = []
    
    # initial split by \n (newline)
    result = result.split("\n")

    # Parse the ClamAV scan results and extract relevant information
    for _ in result:
        if "SUMMARY" not in _ and not SUMMARY:
            [files.append(_.split(":")) if not _ == "" else None]
        elif SUMMARY == False:
            SUMMARY = True
        else:
            leftovers.append(_) if not _.strip() == "" else None
    leftovers = [_.split(":",1) for _ in leftovers]

    # Combine scan results into a dictionary and convert strings to integers
    result = {line[0].strip("    "): line[1].strip() for line in leftovers}

    # Convert scan results to integers (if possible) and remove empty strings
    for _ in result:
        if result[_].isdigit():
            result[_] = int(result[_])

    return files, result

#  TODO replace with actual implementation
def send_email(recipient, subject, body):
    """
    Sends an email using the specified recipient, subject, and body.
    """
    # Replace 'mail' with the path to your mail command
    mail_path = "/usr/bin/mail"
    subprocess.run([mail_path, "-s", subject, recipient], input=body, text=True)
    print(f"Email sent to {recipient}")


if __name__ == "__main__":
    # Example usage
    filename = "test.txt"
    files, scan_results = clam_scan(filename)

    # recipient = "your_email@example.com"
    # subject = "ClamAV Scan Results"
    # body = f"Here are the ClamAV scan results for {filename}:\n\n{scan_results}"
    # send_email(recipient, subject, body)