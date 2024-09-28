import re
from .RecommendationAnalyze import recommendation_algorithm
def split_lines(lines):
    result = []
    current_item = ""
    for line in lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith(
                "4.") or line.startswith("•"):
            if current_item:
                result.append(current_item.strip())
            current_item = line
        else:
            current_item += " " + line
    if current_item:
        result.append(current_item.strip())
    return result


def parse_recommendation(recommendation: str):
    lines = recommendation.split('\n')
    pattern = re.compile(r'^\d+\.\s*\[(.*?)\]\s*$')
    extracted_lists = []

    # print(f"lines: {lines}")

    for line in lines:
        line = line.strip()
        match = pattern.match(line)
        if match:
            list_items = match.group(1).split(',')
            extracted_list = [float(item.strip()) for item in list_items]
            extracted_lists.append(extracted_list)

    return extracted_lists


def get_email_template(detail, recommendation, prompt, email_destination, isAdminister, isDemo):
    detail_list = split_lines(detail.splitlines())
    recommendation, top3_values = recommendation_algorithm(parse_recommendation(recommendation));

    prompt_list = [line.strip() for line in prompt.splitlines() if line.strip()]
    if detail_list and not detail_list[0].startswith("1."):
        detail_list.pop(0)

    formatted_prompt = "<br/><br/>".join(prompt_list)
    formatted_detail = "<br/><br/>".join(detail_list)
    technicians_list = recommendation.to_string(index=False).split('\n')
    formatted_recommendation = "<br/><br/>".join(
        [f"{tech.strip()} Score: {score}" for tech, score in zip(technicians_list, top3_values)]
    )

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                margin: 0;
                padding: 0;
                color: #000000;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #00bbf0;
                color: white;
                padding: 20px;
                text-align: center;
                font-size: 24px;
            }}

            .content {{
                padding: 20px;
                line-height: 1.6;
                color: #000000
            }}

            .footer {{
                background-color: #005792;
                color: white;
                padding: 10px;
                text-align: center;
                font-size: 12px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                font-size: 16px;
                color: white;
                background-color: #00bbf0;
                text-decoration: none;
                border-radius: 5px;
            }}
            .button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                Vehicle Diagnostic ChatBot
            </div>
            <div class="content">
                <p>{f"Dear {email_destination}" if isAdminister else "Dear User"}</p>
                <p><strong></strong><br/>{formatted_prompt}</p>
                <p><strong>Details:</strong><br/>{formatted_detail}</p>
                {'<p><strong>Recommendations:</strong><br/>' + formatted_recommendation + '</p>' if isDemo else ''}
                
                <a href="https://corporate.smartmaintenancesolutions.com/home" class="button">Learn More</a>
            </div>
            <div class="footer">
                &copy; 2024 Smart Maintenance Solutions. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """


def get_rating_email_template(rating : int, userPrompt : str, summary : str):
    prompt_list = [line.strip() for line in userPrompt.splitlines() if line.strip()]
    formatted_summary = "<br/><br/>".join(split_lines(summary.splitlines()))
    formatted_prompt = "<br/><br/>".join(prompt_list)

    return f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #ffffff;
                    margin: 0;
                    padding: 0;
                    color: #000000;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #00bbf0;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    font-size: 24px;
                }}

                .content {{
                    padding: 20px;
                    line-height: 1.6;
                    color: #000000
                }}

                .footer {{
                    background-color: #005792;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    font-size: 12px;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    font-size: 16px;
                    color: white;
                    background-color: #00bbf0;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .button:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    Vehicle Diagnostic ChatBot
                </div>
                <div class="content">
                    <p>Ratings: {rating} / 5</p>
                    <br/>
                    <p><strong></strong><br/>{formatted_prompt}</p>
                    <p><strong></strong><br/>{formatted_summary}</p>

                    <a href="https://corporate.smartmaintenancesolutions.com/home" class="button">Learn More</a>
                </div>
                <div class="footer">
                    &copy; 2024 Smart Maintenance Solutions. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """
