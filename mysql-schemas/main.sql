CREATE DATABASE IF NOT EXISTS `main`;
USE `main`;

CREATE TABLE `Interests` (
  `id` int(11) NOT NULL,
  `slug` varchar(100) NOT NULL
);

CREATE TABLE `People` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `city` varchar(100) NOT NULL
);

CREATE TABLE `PeopleInterests` (
  `id` int(11) NOT NULL,
  `person_id` int(11) NOT NULL,
  `interest_id` int(11) NOT NULL
);

ALTER TABLE `Interests`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `People`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `PeopleInterests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `person` (`person_id`),
  ADD KEY `interest` (`interest_id`);


ALTER TABLE `Interests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `People`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `PeopleInterests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `PeopleInterests`
  ADD CONSTRAINT `interest` FOREIGN KEY (`interest_id`) REFERENCES `Interests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `person` FOREIGN KEY (`person_id`) REFERENCES `People` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

