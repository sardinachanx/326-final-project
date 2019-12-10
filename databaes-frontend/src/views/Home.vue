<template>
  <div class="home">
    <h1>Databaes</h1>
    <div class="img">
      <img src="@/assets/infoScreenshot.png">
    </div>
    <h2 class="quote-1"> "I love it" - Christopher Gomez </h2>
    <h2 class="quote-2"> "Me too" - Christopher Gomez </h2>

    <div class="info">
      <p>Personalized assignment tracking that integrates with course planning:</p>
      <ul>
        <li>Keep track of your assignments and the time you put into them on a class by class basis, increasing time management ability for future class assignments</li>

        <li>Enables planning schedules for upcoming semesters based on the time and effort other students put in</li>
      </ul>
      <p>Overcoming the very real problem of students making ill-informed decisions on future classes for upcoming schedules due to inadequate information from official sources; thereby preventing the range of issues that often result such as the stress and anxiety that often comes from underestimating academics and schedule management.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  components: {
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-height: 600px;
}

h1 {
  font-size: xxx-large;
}

.img {
  transform: translateY(20px) translateX(-400px);
}

.quote-1 {
  transform: translateX(340px) translateY(-260px);
  width: max-content;
}

.quote-2 {
  transform: translateX(540px) translateY(-180px);
  width: max-content;
}

img {
  max-width: 700px;
  border: 2pt solid black;
  animation: rotatecircle 4s infinite linear;
}

@keyframes rotatecircle {
  0% { transform:rotate(0deg); }
  45% { transform:rotate(-15deg) scale(.6); }
  55% { transform:rotate(-345deg) scale(.6); }
  100% { transform:rotate(-360deg); }
}

.info {
  transform: translateY(-90px);
  max-width: 800px;
  text-align: left;
}
</style>
