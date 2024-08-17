const api = axios.create({
  baseURL: 'http://localhost:2139'
});

new Vue({
    el: '#app',
    data: {
        currentSkill: '',
        currentQuestion: '',
        currentTier: '',
        questionIndex: 0,
        message: '',
        error: ''
    },
    mounted() {
        this.getNextSkill();
    },
    methods: {
        getNextSkill() {
            this.error = '';
            api.get('/next-skill')
                .then(response => {
                    if (response.data.skill) {
                        this.currentSkill = response.data.skill;
                        this.currentQuestion = response.data.question;
                        this.currentTier = response.data.tier;
                        this.questionIndex = response.data.questionIndex || 0;
                        this.message = '';
                    } else {
                        this.message = response.data.message;
                        this.currentSkill = '';
                        this.currentQuestion = '';
                        this.currentTier = '';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.error = 'An error occurred while fetching the next skill. Please try again.';
                });
        },
        submitAnswer(answer) {
            this.error = '';
            api.post('/submit-answer', {
                skill: this.currentSkill,
                answer: answer,
                currentTier: this.currentTier,
                questionIndex: this.questionIndex
            })
                .then(response => {
                    if (response.data.question) {
                        this.currentQuestion = response.data.question;
                        this.currentTier = response.data.tier;
                        this.questionIndex = response.data.questionIndex;
                        this.message = '';
                    } else if (response.data.message === 'Skill classified') {
                        this.message = `Skill "${this.currentSkill}" classified as tier ${response.data.tier}`;
                        this.getNextSkill();
                    } else {
                        this.getNextSkill();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    if (error.response && error.response.data && error.response.data.error) {
                        this.error = error.response.data.error;
                    } else {
                        this.error = 'An error occurred while submitting the answer. Please try again.';
                    }
                });
        }
    }
});