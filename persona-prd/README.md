Our work is split between several branches.
Please start here at the main branch
and then continue to integrate-frontend branch.

# persona-prd-hackathon-hyperskill-july-2025 - main branch
PersonaPRD is an AI-powered tool designed 
during the AI Hackathon July 2025.
To transform unstructured community feedback 
into structured Product Requirement Documents (PRDs).
It identifies user pain points, clusters feedback by personas,
and automatically drafts PRD components 
to speed up the ideation phase for product teams.
The main branch goal is to simulate an application flow
with the hard coded data.

To run:
```bash
cd project
git clone https://github.com/Shashank-Shyam-Sunder/persona-prd-hackathon-hyperskill-july-2025.git hack
cd hack/persona-prd
npm install
npm ci
npm run start

```

# persona-prd-hackathon-hyperskill-july-2025 - integrate-frontend branch

After you tried it, please 
```bash
git pull -a
git switch integrate-frontend
```

You will find there a console application 
that implements data processing and clustering.
After that, we converted the console application to API.
Next step, we planned to link FE with BE API,
but we did not have enough time to complete.
Please read integrate-frontend README that explains the flow.