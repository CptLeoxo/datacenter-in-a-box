variable "db_user" {
  description	= "Database user"
  type		= string
}

variable "db_password" {
  description	= "Database password"
  type		= string
  sensitive	= true
}
