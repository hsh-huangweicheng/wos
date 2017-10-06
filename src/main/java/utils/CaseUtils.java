package utils;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CaseUtils {

	private static Pattern pattern = Pattern.compile("(\\w{1})(\\w+)", Pattern.CASE_INSENSITIVE);

	public static String convertCamelCase(String text) {
		Matcher matcher = pattern.matcher(text);

		StringBuffer sb = new StringBuffer();
		int start = 0;

		while (matcher.find()) {

			String firstLetter = matcher.group(1);
			String otherLetter = matcher.group(2);

			sb.append(text.substring(start, matcher.start()));
			sb.append(firstLetter.toUpperCase());
			sb.append(otherLetter.toLowerCase());

			start = matcher.end();
		}

		sb.append(text.substring(start));
		return sb.toString();
	}
}
