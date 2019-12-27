<template>
  <div class="single-question mt-2">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h1>{{ question.content }}</h1>
          <QuestionActions v-if="isQuestionAuthor" :slug="question.slug" />
          <p class="mb-0">
            Posted by:
            <span class="author-name">{{ question.author }}</span>
          </p>
          <p>Created at: {{ question.created_at }}</p>
          <hr />
          <div v-if="userHasAnswered">
            <p class="answer-added">You have answered this question.</p>
          </div>
          <div v-else-if="showForm">
            <form class="card" @submit.prevent="onSubmit">
              <div class="card-header p-3">
                <h5>Answer Here</h5>
              </div>
              <div class="card-block">
                <textarea
                  class="form-control"
                  v-model="newAnswerBody"
                  placeholder="Your answer"
                  rows="5"
                ></textarea>
              </div>
              <div class="card-footer p-3">
                <button type="submit" class="btn btn-sm btn-success">
                  Submit
                </button>
                <button
                  class="btn btn-sm btn-success ml-2"
                  @click="showForm = false"
                >
                  Cancel
                </button>
              </div>
            </form>
            <p v-if="error" class="error mt-2">{{ error }}</p>
          </div>
          <div v-else>
            <button class="btn btn-sm btn-success" @click="showForm = true">
              Answer this question
            </button>
          </div>
          <hr />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <AnswerComponent
            v-for="answer in answers"
            :answer="answer"
            :requestUser="requestUser"
            :key="answer.id"
            @delete-answer="deleteAnswer"
          />
        </div>
        <div class="col-12 my-4 m-3">
          <p v-show="loadingAnswers">Loading...</p>
          <button
            v-show="next"
            @click="getQuestionAnswers"
            class="btn btn-lg btn-success"
          >
            &nabla;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";
import AnswerComponent from "@/components/Answer.vue";
import QuestionActions from "@/components/QuestionActions.vue";

export default {
  name: "Question",
  props: {
    slug: {
      type: String,
      required: true
    }
  },
  components: {
    AnswerComponent,
    QuestionActions
  },
  data() {
    return {
      question: {},
      answers: [],
      newAnswerBody: null,
      error: null,
      userHasAnswered: false,
      showForm: false,
      next: null,
      loadingAnswers: false,
      requestUser: null
    };
  },
  computed: {
    isQuestionAuthor() {
      return this.question.author === this.requestUser;
    }
  },
  methods: {
    setPageTitle(title) {
      document.title = title;
    },
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    getQuestionData() {
      let endpoint = `/api/questions/${this.slug}/`;
      apiService(endpoint).then(data => {
        if (data) {
          this.question = data;
          this.userHasAnswered = data.user_has_answered;
          this.setPageTitle(data.content);
        } else {
          this.$router.push({ name: "page-not-found" });
        }
      });
    },
    getQuestionAnswers() {
      let endpoint = `/api/questions/${this.slug}/answers/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingAnswers = true;
      apiService(endpoint).then(data => {
        this.answers.push(...data.results);
        this.loadingAnswers = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },
    onSubmit() {
      if (this.newAnswerBody) {
        let endpoint = `/api/questions/${this.slug}/answer/`;
        apiService(endpoint, "POST", { body: this.newAnswerBody }).then(
          data => {
            this.answers.unshift(data);
          }
        );
        this.newAnswerBody = null;
        this.showForm = false;
        this.userHasAnswered = true;
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "You can't send an empty answer!";
      }
    },
    async deleteAnswer(answer) {
      let endpoint = `/api/answers/${answer.id}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$delete(this.answers, this.answers.indexOf(answer));
        this.userHasAnswered = false;
      } catch (err) {
        alert(err);
      }
    }
  },
  created() {
    this.setRequestUser();
    this.getQuestionData();
    this.getQuestionAnswers();
  }
};
</script>

<style scoped>
.author-name {
  font-weight: bold;
  color: #dc3545;
}

.answer-added {
  font-weight: bold;
  color: green;
}

.error {
  font-weight: bold;
  color: red;
}
</style>
