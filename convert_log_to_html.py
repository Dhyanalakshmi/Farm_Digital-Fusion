import xml.etree.ElementTree as ET

# Step 1: Read raw log.xml content
log_path = r'C:\Users\Admin\oracle1\diag\tnslsnr\DESKTOP-3H92709\listener\alert\log.xml'

try:
    with open(log_path, 'r', encoding='utf-8') as file:
        raw_xml = file.read()

    # Step 2: Wrap with root <log> tag
    wrapped_xml = f"<log>{raw_xml}</log>"

    # Step 3: Parse the XML content
    root = ET.fromstring(wrapped_xml)

    # Step 4: Create HTML structure
    html = """
    <html>
    <head>
      <title>Oracle Listener Log</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }
        th { background-color: #f4f4f4; }
        tr:nth-child(even) { background-color: #fafafa; }
        h2 { color: #333; }
      </style>
    </head>
    <body>
      <h2>Oracle Listener Logs</h2>
      <table>
        <tr><th>Timestamp</th><th>Log Message</th></tr>
    """

    # Step 5: Populate table rows
    for msg in root.findall('msg'):
        timestamp = msg.get('time', 'N/A')
        text = msg.findtext('txt', '').strip().replace('\n', '<br>')
        html += f"<tr><td>{timestamp}</td><td>{text}</td></tr>"

    # Step 6: Close HTML
    html += """
      </table>
    </body>
    </html>
    """

    # Step 7: Save HTML output
    output_path = 'listener_log.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Log converted successfully! Open '{output_path}' in your browser.")

except Exception as e:
    print(f"❌ Error: {e}")
