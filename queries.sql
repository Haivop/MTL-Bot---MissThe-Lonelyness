SELECT id, name
FROM rules_category
WHERE game_id = self.game_id
  AND parent_id IS NULL

SELECT id, content FROM rules WHERE category_id = {self.rule_id}

SELECT id, name FROM rules_category WHERE parent_id = {self.rule_id}
