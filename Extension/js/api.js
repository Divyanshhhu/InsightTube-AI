const API = {

    BASE_URL: "http://127.0.0.1:8000",

    async post(endpoint, data) {

        const response = await fetch(
            this.BASE_URL + endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        if (!response.ok) {
            throw new Error("Request Failed");
        }

        return await response.json();
    },

    async get(endpoint) {

        const response = await fetch(
            this.BASE_URL + endpoint
        );

        if (!response.ok) {

            const error = await response.text();

            console.error(error);

            throw new Error(error);

        }
        return await response.json();
    }

};