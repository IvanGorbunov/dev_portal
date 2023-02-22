;(function(){
    const myModal = new bootstrap.Modal(document.getElementById('loanApplicationModal'), {
                backdrop: 'static',
                keyboard: false
    })

    htmx.on('htmx:afterSwap', (e) => {
        if(e.detail.target.id === 'loanApplicationDialog' ){
            myModal.show()
        }
    })

    htmx.on("htmx:beforeSwap", (e) => {
        // Empty response targeting #dialog => hide the modal
        if (e.detail.target.id == "loanApplicationDialog" && !e.detail.xhr.response) {
          modal.hide()
          e.detail.shouldSwap = false
        }
      })
    
      // Remove dialog content after hiding
    //   htmx.on("hidden.bs.modal", () => {
    //     document.getElementById("loanApplicationDialog").innerHTML = ""
    //   })

})()