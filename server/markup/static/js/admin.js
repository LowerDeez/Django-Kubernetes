const scroller = function() {
  const links = Array.from(document.getElementsByClassName('sidebar-link'))
  const sidebar = document.getElementsByClassName('sidebar-wrapper')[0]
  const location = window.location.href

  links.forEach(function(link) {
    if (link.classList.contains('clone')) return 
    const link_variant = [
      new RegExp(`^${link.href}$`, ""),
      new RegExp(`^${link.href}add/$`, ""),
      new RegExp(`^${link.href}([^/]+)/?(.*)/change/$`, ""),
    ]
    if(link_variant.find(l => l.exec(location))) {
      const parentSection = link.parentElement.parentElement
      sidebar.scrollTop = parentSection.offsetTop
      link.classList.add('selected')
    }
  })
}
document.addEventListener('DOMContentLoaded', () => {
  scroller()
})