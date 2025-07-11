
var url = "/get_member/"
let data = {
  email: 'member2@gmail.com',
  pass: 'pass'
}
let fetchData = {
  method: 'POST',
  body: JSON.stringify(data),
  headers: new Headers({
    'Content-Type': 'application/json; charset=UTF-8'
  })
}

fetch(url, fetchData)
