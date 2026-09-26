#!/usr/bin/env ruby
#
# Sets last_modified_at for all posts and pages using git log.
# Falls back to the document's date (for posts) or site build time if no git history.
#
# Extended to cover ALL commits (not just multi-commit files) so that every
# URL in sitemap.xml gets a proper <lastmod> value, improving Google crawl signals.

Jekyll::Hooks.register :posts, :post_init do |post|
  lastmod_date = `git log -1 --pretty="%ad" --date=iso "#{post.path}" 2>/dev/null`.strip
  if lastmod_date && !lastmod_date.empty?
    post.data['last_modified_at'] = lastmod_date
  end
end

Jekyll::Hooks.register :pages, :post_init do |page|
  next unless page.path && !page.path.empty?
  full_path = File.join(page.site.source, page.path)
  next unless File.exist?(full_path)
  lastmod_date = `git log -1 --pretty="%ad" --date=iso "#{full_path}" 2>/dev/null`.strip
  if lastmod_date && !lastmod_date.empty?
    page.data['last_modified_at'] = lastmod_date
  end
end
