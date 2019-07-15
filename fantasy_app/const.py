#SELECT
get_user_by_id = 'SELECT * FROM user WHERE id = ?'
get_user_by_username = 'SELECT * FROM user WHERE username = ?'
get_user_likes = 'SELECT distinct postid FROM user_likes WHERE userid = ? and liked = 1'
get_user_dislikes = 'SELECT distinct postid FROM user_likes WHERE userid = ? and disliked = 1'
get_user_id = 'SELECT id FROM user WHERE username = ?'
get_posts = "SELECT p.id, title, body, created, author_id, name, likes, dislikes, comments FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC"
get_comments = 'SELECT * FROM post_comments ORDER BY created DESC'
get_post = 'SELECT p.id, title, body, created, author_id, name, likes, dislikes, comments FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?'
get_likes_count = 'select COUNT(*) from user_likes where postid = ? and liked = 1'
get_dislikes_count = 'select COUNT(*) from user_likes where postid = ? and disliked = 1'
get_comments_count = 'select COUNT(*) from post_comments where postid = ?'
get_post_likes = 'SELECT distinct userid FROM user_likes WHERE postid = ?'

#Insert
insert_user = 'INSERT INTO user (username, password, image, name, nickname, teamid) VALUES (?, ?, ?, ?, ?, ?)'
insert_post = 'INSERT INTO post (title, body, author_id, likes, dislikes, comments)'' VALUES (?, ?, ?, ?, ?, ?)'
insert_user_like = 'INSERT INTO user_likes (userid, postid, liked, disliked)''Values (?,?,?,?)'
insert_post_comment = 'INSERT INTO post_comments (postid, userid, name, comment)''Values (?,?,?,?)'

#Update
update_post = 'UPDATE post SET title = ?, body = ?'' WHERE id = ?'
update_post_counts = 'UPDATE post SET likes = ?, dislikes = ?, comments = ?''where id = ?'
update_post_comments = 'UPDATE post SET comments = comments + 1 WHERE id = ?'
update_user_likes_like = 'UPDATE user_likes SET liked = 1, disliked = 0 WHERE userid = ? and postid = ?'
update_user_likes_unlike = 'UPDATE user_likes SET liked = 0, disliked = 0 WHERE userid = ? and postid = ?'
update_user_likes_dislike = 'UPDATE user_likes SET disliked = 1, liked = 0 WHERE userid = ? and postid = ?'

#Delete
delete_post = 'DELETE FROM post WHERE id = ?'
delete_user_likes = 'DELETE FROM user_likes WHERE postid = ?'
delete_post_comments = 'DELETE FROM post_comments WHERE postid = ?'