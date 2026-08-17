document
  .getElementById("scanform")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const ipAddress = document.getElementById("ipAddress").value;
    const loadingDiv = document.getElementById("loading");
    const resultsDiv = document.getElementById("results");
    const openportslist = document.getElementById("openportslist");
    const display = document.getElementById("display");

    // show loading spinner and hide previous results
    loadingDiv.classList.remove("hidden");
    resultsDiv.classList.add("hidden");
    openportslist.innerHTML = "";

    try {
      // post request to Flask
      const response = await fetch("/scan_ports", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ip: ipAddress }),
      });
      const data = await response.json();

      // hide loading spinner
      loadingDiv.classList.add("hidden");

      if (response.ok) {
        display.textContent = data.ip;

        if (data.open_ports.length > 0) {
          data.open_ports.forEach((port) => {
            const li = document.createElement("li");
            li.textContent = `Port ${port} is open`;
            openportslist.appendChild(li);
          });
        } else {
          const li = document.createElement("li");
          li.textContent = "No open ports found in range 1 - 1024.";
          li.style.color = "#ef4444";
          openportslist.appendChild(li);
        }

        // Show Results
        resultsDiv.classList.remove("hidden");
      } else {
        alert("Error:" + data.error);
      }
    } catch (error) {
      loadingDiv.classList.add("hidden");
      console.error("Error during scan:", error);
      alert("An error occured while connecting to the server.");
    }
  });
