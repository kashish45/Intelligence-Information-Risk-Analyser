
# Intelligence Information Risk Analyser

Information received continuously over emails from various intel sources (mentioned below in the “Deliverables” section) provide details about the incidents that can have a potential impact on the organization. 

We require a text analyzer solution that can read and classify these emails, to understand the potential impact of the incident on the organization, enabling quicker response through proactive monitoring. 

Using technologies like artificial intelligence and machine learning, the analyzer should produce dynamic risk scores, after factoring the organizational data with the incident information. Then, the analyzer should send an event escalation or early warning, based on historical information and patterns. 

# Deliverables
- Propose and design a text analyzer solution (app, dashboard or tool) that will carry out the following tasks:

- The text analyzer takes emails (in a pdf format) as the input.
- From the input mail content, the text analyzer categorizes each email as one of the four source types, based on the email sender’s domain address, as listed below: 
- The text analyzer categorizes each email under one of the ten risk types, based on the keywords.
- The country name gets extracted from the email body.
- A table tracking the total count of inputs, risks, sources, incident severities and countries, gets generated.
- Information from the intel sources are mapped with EY information, to produce country level dynamic risk score by category. 
- The text analyzer evaluates the historical information for a country based on the event type and provides an impact score basis the escalation matrix for the system, to trigger an early warning signal.
- Historical trends of the impact on geography are provided, that indicate seasonality of incidents.
 
- [Intel Information Risk Analyser](https://ey-intel.herokuapp.com/)

## Important Links
- [Intel Information Risk Analyser](https://ey-intel.herokuapp.com/)
- [Intel Information Risk Analyser Dashboard](https://app.powerbi.com/links/rzrDojoSbf?ctid=b868613f-a153-49ec-a06e-990b12559e5f&pbi_source=linkShare)
- [Design Prototype](<iframe width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=7f86f717-cef3-4b69-bc9f-bef454257bf8&autoAuth=true&ctid=b868613f-a153-49ec-a06e-990b12559e5f&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLWluZGlhLWNlbnRyYWwtYS1wcmltYXJ5LXJlZGlyZWN0LmFuYWx5c2lzLndpbmRvd3MubmV0LyJ9" frameborder="0" allowFullScreen="true"></iframe>)
