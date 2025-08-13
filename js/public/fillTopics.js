async function main() {
  let topics = document.getElementById("topics");
  let response = await fetch("/gettopics");
  let data = await response.json();
  data.forEach((item) => {
    let element = document.createElement("option");
    element.textContent = item.path;
    topics.appendChild(element);
  });
}

main();
