$(() => {
  var x = setInterval(function () {
    var now = new Date().getTime();
    distance = countDownDate - now;

    var hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("mytimer").textContent =
      hours + "hr " + minutes + "m " + seconds + "s ";
    if (distance < 0) {
      clearInterval(x);
      document.getElementById("mytimer").innerHTML = "EXPIRED";
      window.location.href = "/OnlineExam/login/submitted/";
    }
  }, 1000);
});
