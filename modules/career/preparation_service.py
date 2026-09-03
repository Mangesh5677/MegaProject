from modules.database.models import Internship, PreparationTask


ARRAY_DSA_PROBLEMS = [
	("Two Sum", "https://leetcode.com/problems/two-sum/"),
	("Best Time to Buy and Sell Stock", "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
	("Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/"),
	("Product of Array Except Self", "https://leetcode.com/problems/product-of-array-except-self/"),
	("Maximum Subarray", "https://leetcode.com/problems/maximum-subarray/"),
	("Maximum Product Subarray", "https://leetcode.com/problems/maximum-product-subarray/"),
	("Find Minimum in Rotated Sorted Array", "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"),
	("Search in Rotated Sorted Array", "https://leetcode.com/problems/search-in-rotated-sorted-array/"),
	("3Sum", "https://leetcode.com/problems/3sum/"),
	("Container With Most Water", "https://leetcode.com/problems/container-with-most-water/"),
	("Move Zeroes", "https://leetcode.com/problems/move-zeroes/"),
	("Merge Sorted Array", "https://leetcode.com/problems/merge-sorted-array/"),
	("Intersection of Two Arrays", "https://leetcode.com/problems/intersection-of-two-arrays/"),
	("Majority Element", "https://leetcode.com/problems/majority-element/"),
	("Missing Number", "https://leetcode.com/problems/missing-number/"),
	("Find the Duplicate Number", "https://leetcode.com/problems/find-the-duplicate-number/"),
	("Rotate Array", "https://leetcode.com/problems/rotate-array/"),
	("Valid Sudoku", "https://leetcode.com/problems/valid-sudoku/"),
	("Spiral Matrix", "https://leetcode.com/problems/spiral-matrix/"),
	("Set Matrix Zeroes", "https://leetcode.com/problems/set-matrix-zeroes/"),
]


def get_task_resources(task):
	text = f"{task.title} {task.category or ''}".lower()
	if "youtube" in text or "video" in text:
		return {
			"youtube": "https://www.youtube.com/results?search_query=array+dsa+problems+leetcode+playlist",
			"problems": [],
		}
	if "dsa" not in text and "array" not in text:
		return []

	return {
		"youtube": "https://www.youtube.com/results?search_query=array+dsa+problems+leetcode+playlist",
		"problems": ARRAY_DSA_PROBLEMS,
	}


def create_preparation_task(db, user_id, internship_id, title, description, category, priority, duration, preparation_date):
	internship = (
		db.query(Internship)
		.filter(Internship.id == internship_id, Internship.user_id == user_id)
		.first()
	)
	if internship is None:
		return None

	task = PreparationTask(
		user_id=user_id,
		internship_id=internship_id,
		title=title.strip(),
		description=description.strip(),
		category=category,
		priority=priority,
		duration=duration,
		preparation_date=preparation_date,
		completed=False,
	)
	db.add(task)
	db.commit()
	db.refresh(task)
	return task


def get_preparation_tasks(db, user_id, internship_id=None):
	query = db.query(PreparationTask).filter(PreparationTask.user_id == user_id)
	if internship_id is not None:
		query = query.filter(PreparationTask.internship_id == internship_id)
	return query.order_by(PreparationTask.completed.asc(), PreparationTask.preparation_date.asc(), PreparationTask.id.desc()).all()


def set_preparation_completed(db, user_id, task_id, completed):
	task = (
		db.query(PreparationTask)
		.filter(PreparationTask.id == task_id, PreparationTask.user_id == user_id)
		.first()
	)
	if task:
		task.completed = completed
		db.commit()
		db.refresh(task)
	return task
