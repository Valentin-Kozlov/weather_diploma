resource "aws_ecr_repository" "front" {
  name                 = "${var.name_project}-front"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_repository" "back" {
  name                 = "${var.name_project}-back"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  encryption_configuration {
    encryption_type = "AES256"
  }

}

resource "aws_ecr_lifecycle_policy" "lifecycle-front" {
  repository = aws_ecr_repository.front.name

  policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
}

resource "aws_ecr_lifecycle_policy" "lifecycle-back" {
  repository = aws_ecr_repository.back.name

  policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 5
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
}
