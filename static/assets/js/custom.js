$(document).on("ready", function () {
  // INITIALIZATION OF DATERANGEPICKER
  $(".js-daterangepicker").daterangepicker();

  $(".js-daterangepicker-times").daterangepicker({
    timePicker: true,
    startDate: moment().startOf("hour"),
    endDate: moment().startOf("hour").add(32, "hour"),
    locale: {
      format: "M/DD hh:mm A",
    },
  });

  var start = moment();
  var end = moment();

  function cb(start, end) {
    $(
      "#js-daterangepicker-predefined .js-daterangepicker-predefined-preview"
    ).html(start.format("MMM D") + " - " + end.format("MMM D, YYYY"));
  }

  $("#js-daterangepicker-predefined").daterangepicker(
    {
      startDate: start,
      endDate: end,
      ranges: {
        Today: [moment(), moment()],
        Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
        "Last 7 Days": [moment().subtract(6, "days"), moment()],
        "Last 30 Days": [moment().subtract(29, "days"), moment()],
        "This Month": [moment().startOf("month"), moment().endOf("month")],
        "Last Month": [
          moment().subtract(1, "month").startOf("month"),
          moment().subtract(1, "month").endOf("month"),
        ],
      },
    },
    cb
  );

  cb(start, end);
});
