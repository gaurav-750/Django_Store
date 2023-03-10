(function (d, m) {
  var kommunicateSettings = {
    appId: "365eb7547a7db02632d1e89c7445acdfa",
    popupWidget: true,
    automaticChatOpenOnNavigation: true,
  };
  var s = document.createElement("script");
  s.type = "text/javascript";
  s.async = true;
  s.src = "https://widget.kommunicate.io/v2/kommunicate.app";
  var h = document.getElementsByTagName("head")[0];
  h.appendChild(s);
  window.kommunicate = m;
  m._globals = kommunicateSettings;
})(document, window.kommunicate || {});
